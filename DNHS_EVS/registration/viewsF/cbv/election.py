from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from registration import forms
from registration.models import Election
from registration.management.helpers.db_object_helpers import toggle_object_status
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
import json

class ElectionList(PermissionRequiredMixin,TemplateView):
    template_name = 'registration/election_list.html'
    permission_required = 'registration.add_election'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['election_filter_form'] = forms.ElectionFilterForm()
        context['show_all_filter_form'] = forms.GenericFilterForm()
        context['modal_ajax_location'] = settings.MODAL_AJAX_LOCATION
        return context

def populate_table_election_list_ajax(request):
    select_all = request.GET.get('select_all')
    school_year = request.GET.get('school_year', None)
    if school_year:
        if select_all == "true":
            election_list = Election.objects.filter(school_year__iexact = school_year)
        else:
            election_list = Election.objects.filter(
                        school_year__iexact = school_year,
                        is_active = True
                        )
    else:
        if select_all == "true":
            election_list = Election.objects.all()
        else:
            election_list = Election.objects.filter(is_active = True)
    json = serializers.serialize('json', election_list)
    return HttpResponse(json, content_type='application/json')

def create_election_ajax(request, *args, **kwargs):
    data = dict()
    context = dict()

    if request.method == 'POST':
        election_form = forms.ElectionForm(data=request.POST)
        if election_form.is_valid():
            election = election_form.save()
            election.created_by = request.user
            election.last_updated_by = request.user
            election.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        election_form = forms.ElectionForm()

    context['mode'] = 'create'
    context['election_form'] = election_form
    data['html_form'] = render_to_string(
            'registration/partial_election_create_ajax.html',
            context,
            request=request
    )
    return JsonResponse(data)

def update_election_ajax(request, pk):
    data = dict()
    context = dict()
    election = get_object_or_404(Election, pk=pk)
    if request.method == 'POST':
        election_form = forms.ElectionForm(request.POST, instance=election)
        if election_form.is_valid():
            election = election_form.save()
            election.last_updated_by = request.user
            election.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        election_form = forms.ElectionForm(instance=election)

    context['mode'] = "update"
    context['election_form'] = election_form
    data['html_form'] = render_to_string(
        'registration/partial_election_create_ajax.html', #reuse the template
        context,
        request=request
    )
    return JsonResponse(data)

def toggle_election_status_ajax(request,pk):
    data = toggle_object_status(object=Election, pk=pk)
    return JsonResponse(data)

def show_more_details_ajax(request, pk):
    data = dict()
    context =  dict()
    position = get_object_or_404(Election, pk = pk)
    form = forms.ElectionFormMoreDetails(instance = position)
    context['mode'] = 'view'
    context['election_form'] = form
    context['object_name'] = 'election'
    data['html_form'] = render_to_string(
        'registration/partial_election_create_ajax.html',
        context,
        request = request
    )
    return JsonResponse(data)
