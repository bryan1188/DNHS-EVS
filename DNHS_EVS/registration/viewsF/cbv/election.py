from django.views.generic import TemplateView
from registration import forms
from registration.models import Election
from django.core import serializers
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
import json

class ElectionList(TemplateView):
    template_name = 'registration/election_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        election_filter_form =  forms.ElectionFilterForm()
        context['election_filter_form'] = election_filter_form
        return context

def populate_table_election_list_ajax(request):
    school_year = request.GET.get('school_year', None)
    if school_year:
        election_list = Election.objects.filter(school_year__iexact=school_year)
    else:
        election_list = Election.objects.all()
    json = serializers.serialize('json', election_list)
    return HttpResponse(json, content_type='application/json')

def create_election_ajax(request):
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

    context['election_form'] = election_form
    data['html_form'] = render_to_string(
            'registration/partial_election_create_ajax.html',
            context,
            request=request
    )
    return JsonResponse(data)
