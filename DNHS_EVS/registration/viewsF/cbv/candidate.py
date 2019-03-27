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

Object = Candidate
Form = forms.CandidateForm
Form_more_details = forms.CandidateFormMoreDetails
_permission_required = 'registration.add_election'

class CandidateList(PermissionRequiredMixin, TemplateView):
    template_name = 'registration/{}.html'.format(Object.__name__.lower())
    permission_required = _permission_required

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modal_ajax_location'] = settings.MODAL_AJAX_LOCATION
        filter_form = forms.GenericFilterForm()
        context['filter_form'] = filter_form
        context['object_name'] = Object.__name__.lower()
        return context

@permission_required(_permission_required, raise_exception=True)
def populate_table_list_ajax(request):
    select_all = request.GET.get('select_all')

    if select_all == "true":
        object_list = Object.all_objects.all()
    else:
        object_list = Object.objects.all()
    return_list = []
    for object in object_list: #create my own json object
        object_json ={}
        object_ = {}
        object_['election'] = object.election.name
        object_['school_year'] = object.election.school_year
        object_['position'] = object.position.__str__()
        object_['student'] = object.student.__str__()
        object_['party'] = object.party.__str__()
        object_['is_active'] = object.is_active
        object_['pk'] = object.id
        object_json['pk'] = object.id
        object_json['fields'] = object_
        return_list.append(object_json)

    return HttpResponse(json.dumps(return_list), content_type='application/json')

@permission_required(_permission_required, raise_exception=True)
def process_post_request(request, form, is_create):
    object = form.save()
    # print(request.POST)
    print(request.FILES)
    if is_create:
        object.created_by = request.user
    object.last_updated_by = request.user
    object.save()

@permission_required(_permission_required, raise_exception=True)
def create_ajax(request, *args, **kwargs):
    data = dict()
    context = dict()

    if request.method =='POST':
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            is_create = True
            process_post_request(request, form, is_create)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = Form()
    context['mode'] = 'create'
    context['form'] = form
    context['object_name'] = Object.__name__.lower()
    data['html_form'] = render_to_string(
        'registration/partial_{}_form_ajax.html'.format(Object.__name__.lower()),
        context,
        request = request
    )
    return JsonResponse(data)

@permission_required(_permission_required, raise_exception=True)
def update_ajax(request, pk):
    data = dict()
    context = dict()
    object = get_object_or_404(Object.all_objects.all(), pk = pk)
    if request.method == 'POST':
        form = Form(request.POST, request.FILES, instance = object)
        if form.is_valid():
            is_create = False
            process_post_request(request, form, is_create)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = Form(instance = object)

    context['mode'] = 'update'
    context['form'] = form
    context['object_name'] = Object.__name__.lower()
    data['html_form'] = render_to_string(
        'registration/partial_{}_form_ajax.html'.format(Object.__name__.lower()),
        context,
        request=request
    )
    return JsonResponse(data)

@permission_required(_permission_required, raise_exception=True)
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

@permission_required(_permission_required, raise_exception=True)
def toggle_status_ajax(request,pk):
    data = toggle_object_status(object = Object, pk = pk)
    return JsonResponse(data)

@permission_required(_permission_required, raise_exception=True)
def show_more_details_ajax(request, pk):
    data = dict()
    context = dict()
    object = get_object_or_404(Object.all_objects.all(), pk=pk)
    form = Form_more_details(instance=object)

    context['mode'] = 'view'
    context['form'] = form
    context['object_name'] = Object.__name__.lower()
    data['html_form'] = render_to_string(
        'registration/partial_{}_form_ajax.html'.format(Object.__name__.lower()),
        context,
        request=request
    )
    return JsonResponse(data)
