from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views.generic import TemplateView
from reporting.forms import ElectionFilterForm
from reporting import forms
from registration.models import Election,Voter
from reporting.models import (DenormalizedVotes,WinnerCandidateDenormalized,
                                ParticipationRate
                             )
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from reporting.management.helpers.color_picker import ColorPicker
from django.template.loader import render_to_string

_permission_required = 'registration.view_vote'

class Reporting(PermissionRequiredMixin,TemplateView):
    permission_required = _permission_required
    template_name = 'reporting/reports.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['election_filter_form'] = ElectionFilterForm()
        context['result_filter_form'] = forms.ElectionResultFilterForm()
        # context['default_election'] = Election.objects.filter(status='COMPLETED').first()
        # context['default_distribution'] ="section"
        context['participation_rate_filter'] = forms.ElectionResultFilterForm()
        return context

@permission_required(_permission_required, raise_exception=True)
def get_votes_distribution_ajax(request):
    distribution_by_title_text = {
        "voter_class_section": "Section",
        "voter_class_grade_level": "Grade Level",
        "voter_sex": "Gender",
        "voter_age": "Age",
        "voter_address_barangay": "Barangay Address",
    }
    election_id = request.GET.get('election')
    distribution_by = request.GET.get('distribution')

    distribution_by_data = list()
    html_panel = ""
    # use in id of canvas as prefix identifier
    nav_pill = 'votes-distribution'

    if election_id:
        election = Election.objects.get(id=election_id)
        positions = election.positions.all()
        query_set = DenormalizedVotes.objects.get_votes_distribution(
                election_id,distribution_by
        )
        # build a dictionary of every position containing the distribution_by data
        # this way, it is easy to render on the template

        for position in positions:
            position_dict = dict()
            color_picker = ColorPicker()
            color_picker.opacity = .5
            '''
                Dictionary Format:
                {
                    position: <position>,
                    title_text: <Title of the chart. used in options.title.text>,
                    labels: [list of the distribution_by data],
                    dataset: [ <list of dictionary>
                        {
                            label: <candidate_name>,
                            data: [votes per distribution_by],
                            backgroundColor: <get from ColorPicker() helper>,
                            borderWidth: 1
                        }
                    ]
                }
            '''
            position_dict['position'] = str(position)
            position_dict['title_text'] = "Voters Distribution by {}".format(
                                    distribution_by_title_text.get(distribution_by,"_")
            )
            position_query_set =  query_set.filter(candidate_position=str(position))
            labels = [
                        row[distribution_by] \
                        for row in position_query_set
                        ]
            labels = list(set(labels))
            labels.sort()
            position_dict['labels'] = labels #to remove duplicate, convert to set then convert back to list
            dataset_list = list()

            # get all candidates for this position
            candidates = [
                        row['candidate_name'] \
                        for row in position_query_set
                        ]

            candidates = list(set(candidates)) #remove dups
            candidates.sort() #sort it back

            #create the dataset dictionary for each candidate
            for candidate in candidates:
                dataset_dict = dict()
                dataset_dict['label'] = candidate
                dataset_data_list = list()
                #check the query set and get the data for each group of column
                for label in position_dict['labels']:
                    data_found_flag = False #  use to determine if data is found for
                        # the specific candidate and distribution_by item
                    for row in  query_set.filter(
                        candidate_position=str(position),
                        candidate_name=candidate
                        ):
                        if row[distribution_by] == label: #this is the data
                            dataset_data_list.append(row['votes']) #append it
                            data_found_flag = True
                    if not data_found_flag:
                        dataset_data_list.append(0)
                dataset_dict['data'] = dataset_data_list
                dataset_dict['backgroundColor'] = color_picker.get_random_color()
                dataset_dict['borderWidth'] = 1
                dataset_list.append(dataset_dict)

            #replace space with dash(-) to avoid issue in html upon using this as id
            position_as_id = str(position).replace(' ','-').lower()
            position_dict['object_id'] = position_as_id
            position_dict['dataset'] =  dataset_list
            distribution_by_data.append(position_dict)

            # create html for the panel to be inserted in the template
            context = dict()
            #identifies if the panel to be made is for primary.
            #difference is on the padding,margin, etc. style
            context['primary_panel_flag'] = False
            context['object_id'] = position_as_id
            context['nav_pill'] = nav_pill
            context['panel_title'] = position
            context['tabular_3_col_name'] = distribution_by_title_text.get(distribution_by,"_")
            context['position_query_set'] = position_query_set.values_list(
                            'candidate_position',
                            'candidate_name',
                            distribution_by,
                            'votes'
            )
            html_panel += render_to_string(
                    'reporting/partial_panel_pane.html',
                    context,
                    request=request
            )

    return JsonResponse({
                'result_data': distribution_by_data,
                'html_panel': html_panel,
                'nav_pill': nav_pill
                }
    )

@permission_required(_permission_required, raise_exception=True)
def populate_winner_table_ajax(request):
    '''
    '''
    election_id = request.GET.get('election')
    winners_query_set = WinnerCandidateDenormalized.objects.filter(
                            election_id=election_id
                            )
    return_data = serializers.serialize(
            'json',
            list(winners_query_set),
            fields=(
            'candidate_position',
            'candidate_name',
            'candidate_party',
            'number_of_votes'
            )
    )
    return HttpResponse(return_data, content_type='application/json')

@permission_required(_permission_required, raise_exception=True)
def populate_result_graphs_ajax(request):
    '''
    '''
    election_id = request.GET.get('election')
    # election_id = 1 #for testing only
    # list of dictionaries. each dictionary represents a graph's data
    result_data = list()
    html_panel = ""
    nav_pill = 'election-result'

    if election_id:
        color_picker = ColorPicker()
        color_picker.opacity = 1
        election = Election.objects.get(id=election_id)
        positions = election.positions.all()
        #get group_by data
        votes_per_candidate_qs = DenormalizedVotes.objects.get_votes_per_candidate(
                        election_id=election_id
                        )

        for position in positions:
            #build dictionary of graphs for all positions
            #same format used in get_votes_distribution_ajax
            position_result = dict()
            position_graph_background_color = color_picker.get_random_color()
            '''
                Dictionary Format:
                {
                    position: <position>,
                    title_text: <Title of the chart. used in options.title.text>,
                    labels: [list of candidates],
                    dataset:
                        {
                            label: <Position>,
                            data: [vote_count per candidate],
                            backgroundColor: [get from CollorPicker()],
                            borderWidth: 1
                        }
                }
            '''
            position_result['position'] = str(position)
            position_result['title_text'] = 'Votes count for {}'.format(str(position))
            position_result['labels'] = [
                        candidate['candidate_name'] \
                        for candidate in votes_per_candidate_qs.filter(
                            candidate_position=position
                        )
            ]
            dataset_list = list()
            dataset = dict()
            dataset['label'] = str(position)
            dataset['data'] = [
                    candidate['votes'] \
                    for candidate in votes_per_candidate_qs.filter(
                        candidate_position=position
                        )
            ]
            dataset['backgroundColor'] = [
                    position_graph_background_color \
                    for x in range(len(position_result['labels']))
            ]
            dataset['borderWidth'] = 1

            # check for canidates that got zero votes
            canidates_ = election.candidates.all().filter(
                        position__title=position
            )
            candidate_list = [
                    str(candidate.student) \
                    for candidate in canidates_
            ]
            # check for difference
            # https://stackoverflow.com/questions/3462143/get-difference-between-two-lists
            diff_candidates = list(set(candidate_list) - set(position_result['labels']))
            if diff_candidates:
                # add the candidates in the list
                for candidate in diff_candidates:
                    position_result['labels'].append(candidate)
                    dataset['data'].append(0)
                    dataset['backgroundColor'].append(position_graph_background_color)

            dataset_list.append(dataset)
            position_result['dataset'] = dataset_list
            position_as_id = str(position).replace(' ','-').lower()
            position_result['object_id'] = position_as_id
            result_data.append(position_result)

            # create html for the panel to be inserted in the template
            context = dict()
            #identifies if the panel to be made is for primary.
            #difference is on the padding,margin, etc. style
            context['primary_panel_flag'] = False
            context['object_id'] = position_as_id
            context['nav_pill'] = nav_pill
            context['panel_title'] = position
            context['tabular_3_col_name'] = "Party"
            context['position_query_set'] = votes_per_candidate_qs.values_list(
                            'candidate_position',
                            'candidate_name',
                            'candidate_party',
                            'votes'
            ).filter(candidate_position=position)
            html_panel += render_to_string(
                    'reporting/partial_panel_pane.html',
                    context,
                    request=request
            )

    return JsonResponse({
                'result_data': result_data,
                'html_panel': html_panel,
                'nav_pill': nav_pill
                }
    )

@permission_required(_permission_required, raise_exception=True)
def populate_participation_report_graphs_overall_ajax(request):
    '''
    '''
    election_id = request.GET.get('election')
    result_data = list()
    # make the the html for the panels needed
    html_panel = ""
    nav_pill = 'participation-rate'

    if election_id:
        election = Election.objects.get(id=election_id)
        # create dictionary needed for overall data
        '''
            Dictionary Format:
            {
                title_text: <Title of the chart. used in options.title.text>,
                text_center: <percentage>
                labels: ['voted', 'not voted'],
                dataset:
                    {
                        label: 'Participation Rate',
                        data: [<#of voted>,<# not voted>],
                        backgroundColor: [gree,red],
                        borderWidth: 1
                    }
            }
        '''
        participation_report_overall_dict = dict()
        participation_report_overall_dict['title_text'] = 'Overall Participation Rate'
        participation_report_overall_dict['labels'] = ['Voted', 'Not Voted']
        dataset_list = list()
        dataset_dict = dict()
        dataset_dict['label'] = 'Participation Rate'
        overall_query_set = ParticipationRate.objects.filter(
                                    election_id=election_id,
                                    group='OVERALL'
                                ).first()
        dataset_dict['data'] = [
                        overall_query_set.total_casted_votes,
                        overall_query_set.total_not_voted
        ]
        dataset_dict['backgroundColor'] = [
                        "rgba(103, 201, 64, 1)",
                        "rgba(252, 68, 86, 1)"
        ]
        dataset_dict['borderWidth'] = 1
        if overall_query_set.total_voters:
            participation_report_overall_dict['center_text'] =  '{}%'.format(
                        round(overall_query_set.total_casted_votes/overall_query_set.total_voters * 100 , 2)
                    )
        else:
            participation_report_overall_dict['center_text'] =  '0%'
        dataset_list.append(dataset_dict)
        participation_report_overall_dict['dataset'] = dataset_list
        participation_report_overall_dict['object_id'] = 'overall'
        result_data.append(participation_report_overall_dict)
        context = dict()
        #identifies if the panel to be made is for primary.
        #difference is on the padding,margin, etc. style
        context['primary_panel_flag'] = True
        context['object_id'] = 'overall'
        context['nav_pill'] = nav_pill
        context['panel_title'] = 'Overall'
        voters_query_set = Voter.objects.filter(
                                election=election
                            ).prefetch_related('student_class')
        voters_tuple = [ (
                            voter.student_class.grade_level,
                            voter.student_class.section,
                            str(voter),
                            'Yes' if voter.is_vote_casted else 'No'
                         ) \
                            for voter in voters_query_set
                       ]
        context['tabular_query_set'] = voters_tuple

        html_panel += render_to_string(
                'reporting/partial_panel_pane_participation.html',
                context,
                request=request
        )
    return JsonResponse({
                'result_data': result_data,
                'html_panel': html_panel,
                'nav_pill': nav_pill
                }
    )

@permission_required(_permission_required, raise_exception=True)
def populate_participation_report_graphs_ajax(request):
    '''
    '''
    election_id = request.GET.get('election')
    # election_id = 1
    print(election_id)
    result_data = list()
    # make the the html for the panels needed
    html_panel = ""
    nav_pill = 'participation-rate'

    if election_id:
        election = Election.objects.get(id=election_id)
        # create dictionary needed for grade_level report
        '''
            Dictionary Format:
            {
                title_text: <Title of the chart. used in options.title.text>,
                labels: [list of candidates],
                object_id: <object_identifier>
                dataset:
                    {
                        data: [participation_rate per grade_level],
                        backgroundColor: [get from CollorPicker()],
                        borderWidth: 1
                    }
            }
        '''
        grade_level_graph_dict = dict()
        grade_level_color_picker = ColorPicker()
        grade_level_color_picker.opacity = .6
        grade_level_graph_dict['title_text'] = "Participation Rate per Grade Level"
        grade_level_query_set = ParticipationRate.objects.filter(
                election_id=election_id,
                group='GRADE_LEVEL'
                )
        grade_level_graph_dict['labels'] =list(
                    grade_level_query_set.values_list('group_value', flat=True)
        )
        grade_level_graph_dict['object_id'] = 'grade_level'
        dataset_list = list()
        dataset_dict = dict()
        dataset_dict['data'] = [
                round(row * 100, 2) for row in \
                        grade_level_query_set.values_list('percentage', flat=True)
        ]
        dataset_dict['backgroundColor'] = [
                grade_level_color_picker.get_random_color() \
                for x in range(len(dataset_dict['data']))
        ]
        dataset_dict['borderWidth'] = 1
        dataset_list.append(dataset_dict)
        grade_level_graph_dict['dataset'] = dataset_list
        result_data.append(grade_level_graph_dict)

        # create html for the panel to be inserted in the template
        context = dict()
        #identifies if the panel to be made is for primary.
        #difference is on the padding,margin, etc. style
        context['primary_panel_flag'] = False
        context['object_id'] = grade_level_graph_dict['object_id']
        context['nav_pill'] = nav_pill
        context['panel_title'] = "By Grade Level"
        context['tabular_1_col_name'] = "Grade Level"
        context['tabular_query_set'] = [(
                    row.group_value,
                    row.total_voters,
                    row.total_casted_votes,
                    round(row.percentage * 100 , 2)
                ) \
                for row in grade_level_query_set
        ]
        html_panel += render_to_string(
                'reporting/partial_panel_pane_participation.html',
                context,
                request=request
        )

        # create dictionary needed for section level report
        '''
            Dictionary Format:
            {
                title_text: <Title of the chart. used in options.title.text>,
                labels: [list of candidates],
                object_id: <object_identifier>
                dataset:
                    {
                        data: [participation_rate per section],
                        backgroundColor: [get from CollorPicker()],
                        borderWidth: 1
                    }
            }
        '''
        section_graph_dict = dict()
        section_color_picker = ColorPicker()
        section_color_picker.opacity = .6
        section_graph_dict['title_text'] = "Participation Rate per Section"
        section_query_set = ParticipationRate.objects.filter(
                election_id=election_id,
                group='SECTION'
                )
        section_graph_dict['labels'] =list(
                    section_query_set.values_list('group_value', flat=True)
        )
        section_graph_dict['object_id'] = 'section'
        dataset_list = list()
        dataset_dict = dict()
        dataset_dict['data'] = [
                round(row * 100, 2) for row in \
                        section_query_set.values_list('percentage', flat=True)
        ]
        dataset_dict['backgroundColor'] = [
                section_color_picker.get_random_color() \
                for x in range(len(dataset_dict['data']))
        ]
        dataset_dict['borderWidth'] = 1
        dataset_list.append(dataset_dict)
        section_graph_dict['dataset'] = dataset_list
        result_data.append(section_graph_dict)

        # create html for the panel to be inserted in the template
        context = dict()
        #identifies if the panel to be made is for primary.
        #difference is on the padding,margin, etc. style
        context['primary_panel_flag'] = False
        context['object_id'] = section_graph_dict['object_id']
        context['nav_pill'] = nav_pill
        context['panel_title'] = "By Section"
        context['tabular_1_col_name'] = "Section"
        context['tabular_query_set'] = [(
                    row.group_value,
                    row.total_voters,
                    row.total_casted_votes,
                    round(row.percentage * 100 , 2)
                ) \
                for row in section_query_set
        ]
        html_panel += render_to_string(
                'reporting/partial_panel_pane_participation.html',
                context,
                request=request
        )


    return JsonResponse({
                'result_data': result_data,
                'html_panel': html_panel,
                'nav_pill': nav_pill
                }
    )
