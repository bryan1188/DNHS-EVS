from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views.generic import DetailView,TemplateView
from registration.models import Election,Candidate,Vote
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string
from reporting.management.helpers.color_picker import ColorPicker

class ElectionLiveMonitoring(PermissionRequiredMixin, TemplateView):
    permission_required = 'registration.view_vote'
    template_name = 'election/election_live_monitoring.html'
    model = Election

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Election.objects.get_current_election()
        return context

@permission_required('registration.view_vote', raise_exception=True)
def populate_vote_count_ajax(request):
    election = Election.objects.get_current_election()
    return_list = []
    for candidate in election.candidates.all():
        object_json = {}
        object_ = {}
        object_['position'] = candidate.position.__str__()
        object_['candidate'] = candidate.student.__str__()
        object_['vote_count'] = candidate.votes.count()
        object_['number_of_slots'] = candidate.position.number_of_slots
        object_['candidate_id'] = candidate.id
        object_['potential_winner'] = False #to be updated later
        object_json['fields'] = object_
        return_list.append(object_json)

    #create list of candidates who are potential winners
    """
        1. Get all positions for the current election
        2. for each election, get the canidates from return_list dict
        3. sort by using lambda
            sorted(candidate, key = lambda key_:key_['fields']['vote_count'], reverse=True)
        4. based on number of slot, identify the potential winner candidate
    """
    position_list = election.positions.all()
    potential_winners_id = set()

    for position in position_list:
        # filter from retun_list
        candidates_for_position = [candidate for candidate in return_list \
                                if candidate['fields']['position'] == position.title]
        # sort the candidates according to number of votes
        candidates_for_position = sorted(candidates_for_position,
                                key = lambda key_:key_['fields']['vote_count'],
                                reverse = True
        )
        number_of_slots = position.number_of_slots
        counter = 0
        while number_of_slots > 0 and len(candidates_for_position) > counter:
            # check for non zero votes
            if candidates_for_position[counter]['fields']['vote_count'] > 0:
                potential_winners_id.add(
                    candidates_for_position[counter]['fields']['candidate_id']
                )
                # check for a tie
                if number_of_slots == 1:
                    vote_count_to_check = candidates_for_position[counter]['fields']['vote_count']
                    # check other candidates that has the same number of votes
                    candidates_in_tie = [candidate['fields']['candidate_id'] \
                                        for candidate in candidates_for_position \
                                        if candidate['fields']['vote_count'] == vote_count_to_check]
                    potential_winners_id.update(candidates_in_tie)
            counter += 1
            number_of_slots -= 1

    #update the potential_winner field
    for candidate in return_list:
        if candidate['fields']['candidate_id'] in potential_winners_id:
            candidate['fields']['potential_winner'] = True
    return HttpResponse(json.dumps(return_list), content_type='application/json')

@permission_required('registration.view_vote', raise_exception=True)
def check_for_new_vote_ajax(request):
    '''
        This function will check if there is new vote casted based on vote.created_date
            Max date. It will compare the client last update to this max value
    '''
    data = dict()
    last_vote_timestamp = Vote.objects.get_last_create_date()
    data['last_vote_timestamp'] = str(last_vote_timestamp.year) \
                        + str(last_vote_timestamp.month) \
                        + str(last_vote_timestamp.day) \
                        + str(last_vote_timestamp.hour) \
                        + str(last_vote_timestamp.minute) \
                        + str(last_vote_timestamp.second)
    return JsonResponse(data)

def bar_graph_data_creator(by_identifier, data):
    # create dictionary needed for grade_level report
    '''
        Dictionary Format:
        {
            title_text: <Title of the chart. used in options.title.text>,
            labels: [list of grade_level/section],
            object_id: <object_identifier>
            dataset:
                {
                    data: [participation_rate per grade_level/section],
                    backgroundColor: [get from CollorPicker()],
                    borderWidth: 1
                }
        }
    '''
    grade_level_graph_dict = dict()
    grade_level_color_picker = ColorPicker()
    grade_level_color_picker.opacity = .6
    grade_level_graph_dict['title_text'] = "Participation Rate per {}".format(by_identifier)
    grade_level_graph_dict['labels'] =[ item['grade_level_or_section'] \
                     for item in data
    ]
    dataset_list = list()
    dataset_dict = dict()
    dataset_dict['data'] = [ item['participation_rate'] \
                     for item in data
    ]
    dataset_dict['backgroundColor'] = [
            grade_level_color_picker.get_random_color() \
            for x in range(len(dataset_dict['data']))
    ]
    dataset_dict['borderWidth'] = 1
    dataset_list.append(dataset_dict)
    grade_level_graph_dict['dataset'] = dataset_list
    return grade_level_graph_dict

@permission_required('registration.view_vote', raise_exception=True)
def populate_participation_rate_ajax(request):
    context = dict()

    # get list of voters
    election = Election.objects.get_current_election()
    voters = election.voters.all().order_by(
                'student_class__grade_level_integer',
                'student__family_name'
            )
    context['voters'] = voters

    # get grade_level participation_rate
    context['grade_level_participation_rate'] = election.grade_level_participation_rate_dict

    # get section participation_rate
    context['section_participation_rate'] =  election.section_participation_rate_dict

    #get overall participation_rate
    overall_participation_rate = election.participation_rate
    overall_participation_rate_graph = dict()
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
    overall_participation_rate_graph['title_text'] = 'Overall Participation Rate'
    overall_participation_rate_graph['labels'] = ['Voted', 'Not Voted']
    dataset_list = list()
    dataset_dict = dict()
    dataset_dict['label'] = 'Participation Rate'
    dataset_dict['data'] = [
                    overall_participation_rate['number_voted'],
                    overall_participation_rate['number_not_voted']
    ]
    dataset_dict['backgroundColor'] = [
                    "rgba(103, 201, 64, 1)",
                    "rgba(252, 68, 86, 1)"
    ]
    dataset_dict['borderWidth'] = 1
    overall_participation_rate_graph['center_text'] = "{}%".format(overall_participation_rate['participation_rate'])
    dataset_list.append(dataset_dict)
    overall_participation_rate_graph['dataset'] = dataset_list

    grade_level_graph_dict = bar_graph_data_creator("Grade Level", context['grade_level_participation_rate'])
    section_graph_dict = bar_graph_data_creator("Section", context['section_participation_rate'])

    html_panel = render_to_string(
        'election/partial_election_live_participation_rate.html',
        context,
        request=request
    )
    return JsonResponse({
        'html_panel': html_panel,
        'overall_participation_rate_graph': overall_participation_rate_graph,
        'grade_level_graph_dict': grade_level_graph_dict,
        'section_graph_dict': section_graph_dict
    })
