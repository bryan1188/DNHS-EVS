from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from registration import forms
from registration.models import Election
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
        election_filter_form =  forms.ElectionFilterForm()
        context['election_filter_form'] = election_filter_form
        context['modal_ajax_location'] = settings.MODAL_AJAX_LOCATION
        return context

def populate_table_election_list_ajax(request):
    school_year = request.GET.get('school_year', None)
    if school_year:
        election_list = Election.objects.filter(school_year__iexact=school_year)
    else:
        election_list = Election.objects.all()
    json = serializers.serialize('json', election_list)
    return HttpResponse(json, content_type='application/json')

def create_election_ajax(request, *args, **kwargs):
    data = dict()
    context = dict()

    if request.method == 'POST':
        election_form = forms.ElectionForm(data=request.POST)
        if election_form.is_valid():
            election = election_form.save(commit=False)
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
            election = election_form.save(commit=False)
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
