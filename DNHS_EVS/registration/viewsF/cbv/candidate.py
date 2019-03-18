from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from registration import forms
from registration.models import Candidate,Election,Student
from registration.models_election import Position,PositionGradeLevel
from registration.management.helpers.db_object_helpers import toggle_object_status
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings
import json

class CandidateList(PermissionRequiredMixin, TemplateView):
    template_name = 'registration/candidate.html'
    permission_required = 'registration.add_election'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modal_ajax_location'] = settings.MODAL_AJAX_LOCATION
        filter_form = forms.GenericFilterForm()
        context['filter_form'] = filter_form
        context['object_name'] = 'candidate'
        return context

@permission_required('registration.add_election', raise_exception=True)
def populate_table_list_ajax(request):
    select_all = request.GET.get('select_all')

    if select_all == "true":
        object_list = Candidate.all_objects.all()
    else:
        object_list = Candidate.objects.all()
    json = serializers.serialize('json', object_list,
            use_natural_foreign_keys=True,
            use_natural_primary_keys=True,
        )
    return HttpResponse(json, content_type='application/json')

def process_post_request(request, form, is_create):
    object = form.save()
    if is_create:
        object.created_by = request.user
    object.last_updated_by = request.user
    object.save()

@permission_required('registration.add_election', raise_exception=True)
def create_ajax(request, *args, **kwargs):
    data = dict()
    context = dict()

    if request.method =='POST':
        form = forms.CandidateForm(data = request.POST)
        if form.is_valid():
            is_create = True
            process_post_request(request, form, is_create)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = forms.CandidateForm()
    context['mode'] = 'create'
    context['form'] = form
    context['object_name'] = 'candidate'
    data['html_form'] = render_to_string(
        'registration/partial_candidate_form_ajax.html',
        context,
        request = request
    )
    return JsonResponse(data)

@permission_required('registration.add_election', raise_exception=True)
def populate_options_for_student_ajax(request):
    data = dict()
    context = dict()
    election_id = request.GET.get('election',None)
    if election_id:
        election = get_object_or_404(Election, pk = election_id)
        student_list_ = Student.objects.filter(
            classes__school_year = election.school_year
        )
        position_list = election.positions.all()
        school_year = election.school_year
        student_list = []
        for student in student_list_:
            student_dict = dict()
            student_dict['id'] = student.id
            student_dict['name'] = student
            student_dict['current_class'] = student.classes.filter(
                school_year=election.school_year
                ).first().grade_level_section
            student_list.append(student_dict)
    else:
        student_list = None
        position_list = None
        school_year = None
    data['student_list_html'] = render_to_string(
        'registration/partial_dropdown_list_options_student.html',
        {
        'objects': student_list,
        'school_year': school_year,
        },
        request = request,
    )
    data['position_list_html'] = render_to_string(
        'registration/partial_dropdown_list_options.html',
        {
        'objects': position_list
        },
        request = request,
    )
    return JsonResponse(data)
