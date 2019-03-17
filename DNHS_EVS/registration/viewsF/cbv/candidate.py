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
        position_list = Candidate.all_objects.all()
    else:
        position_list = Candidate.objects.all()

@permission_required('registration.add_election', raise_exception=True)
def create_ajax(request, *args, **kwargs):
    data = dict()
    context = dict()

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
