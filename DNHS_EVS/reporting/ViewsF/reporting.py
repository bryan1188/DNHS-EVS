from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views.generic import TemplateView
from reporting.forms import ElectionFilterForm
from reporting import forms
from registration.models import Election
from reporting.models import DenormalizedVotes
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
        context['default_election'] = Election.objects.filter(status='COMPLETED').first()
        context['default_distribution'] ="section"
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
            color_picker.opacity = .4
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
            position_dict['labels'] = list(set(labels)) #to remove duplicate, convert to set then convert back to list
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
            position_dict['position_as_id'] = position_as_id
            position_dict['dataset'] =  dataset_list
            distribution_by_data.append(position_dict)

            # create html for the panel to be inserted in the template
            context = dict()
            context['position'] = position_as_id
            context['position_complete'] = position
            context['distrbution_by'] = distribution_by_title_text.get(distribution_by,"_")
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
                'distribution_by_data': distribution_by_data,
                'html_panel': html_panel
                }
    )
