from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from registration import forms
from registration.models import Party
from registration.models_election import Position,PositionGradeLevel
from registration.management.helpers.db_object_helpers import toggle_object_status
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings
import json

class PartyList(PermissionRequiredMixin, TemplateView):
    template_name = 'registration/party.html'
    permission_required = 'registration.add_election'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modal_ajax_location'] = settings.MODAL_AJAX_LOCATION
        filter_form = forms.GenericFilterForm()
        context['filter_form'] = filter_form
        return context

@permission_required('registration.add_election', raise_exception=True)
def populate_table_party_list_ajax(request):
    select_all = request.GET.get('select_all')
    if select_all == "true":
        party_list = Party.all_objects.all()
    else:
        party_list = Party.objects.all()
    json = serializers.serialize('json', party_list)
    return HttpResponse(json, content_type='application/json')

@permission_required('registration.add_election', raise_exception=True)
def process_post_request(request, form, is_create):
    party = form.save()
    if is_create:
        party.created_by = request.user
    party.last_updated_by = request.user
    party.save()

@permission_required('registration.add_election', raise_exception=True)
def create_ajax(request, *args, **kwargs):
    data = dict()
    context = dict()

    if request.method == 'POST':
        form = forms.PartyForm(data = request.POST)
        if form.is_valid():
            is_create = True
            process_post_request(request, form, is_create)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = forms.PartyForm()

    context['mode'] = 'create'
    context['form'] = form
    context['object_name'] = 'party'
    data['html_form'] = render_to_string(
            'registration/partial_party_form_ajax.html',
            context,
            request = request
    )
    return JsonResponse(data)

@permission_required('registration.add_election', raise_exception=True)
def update_ajax(request, pk):
    data = dict()
    context = dict()
    party = get_object_or_404(Party.all_objects.all(), pk = pk)
    if request.method == 'POST':
        form = forms.PartyForm(request.POST, instance = party)
        if form.is_valid():
            is_create = False
            process_post_request(request, form, is_create)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = forms.PartyForm(instance = party)

    context['mode'] = 'update'
    context['form'] = form
    context['object_name'] = 'party'
    data['html_form'] = render_to_string(
            'registration/partial_party_form_ajax.html',
            context,
            request = request
    )
    return JsonResponse(data)

@permission_required('registration.add_election', raise_exception=True)
def toggle_status_ajax(request,pk):
    data = toggle_object_status(object=Party, pk=pk)
    return JsonResponse(data)

@permission_required('registration.add_election', raise_exception=True)
def show_more_details_ajax(request, pk):
    data = dict()
    context = dict()
    party = get_object_or_404(Party.all_objects.all(), pk = pk)
    form = forms.PartyFormMoreDetails(instance = party)
    context['mode'] = 'view'
    context['form'] = form
    context['object_name'] = 'party'
    data['html_form'] = render_to_string(
            'registration/partial_party_form_ajax.html',
            context,
            request = request
    )
    return JsonResponse(data)
