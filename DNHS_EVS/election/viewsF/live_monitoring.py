from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views.generic import DetailView,TemplateView
from registration.models import Election,Candidate,Vote
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json
from django.utils import timezone
from django.http import JsonResponse

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
        object_json['fields'] = object_
        return_list.append(object_json)

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
