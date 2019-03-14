from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from registration import forms
from registration.models import Election
from registration.models_election import Position,PositionGradeLevel
from registration.management.helpers.db_object_helpers import toggle_object_status
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings
import json

class PositionList(PermissionRequiredMixin, TemplateView):
    template_name = 'registration/position.html'
    permission_required = 'registration.add_election'

    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['modal_ajax_location'] = settings.MODAL_AJAX_LOCATION
        return context

def populate_table_position_list_ajax(request):
    position_list = Position.objects.all()
    return_list = []
    for position in position_list: #create my own json object
        position_json ={}
        position_ = {}
        position_['title'] = position.title
        position_['number_of_slots'] = position.number_of_slots
        position_['pk'] = position.id
        grade_levels =  position.grade_levels.all().values_list(
                                    'grade_level',
                                    flat=True
                                    )
        position_['grade_level'] = [grade_level for grade_level in grade_levels]
        position_['is_active'] = 'Active' if position.is_active else 'Inactive'
        position_json['pk'] = position.id
        position_json['fields'] = position_
        return_list.append(position_json)

    return HttpResponse(json.dumps(return_list), content_type='application/json')

def process_post_request(request, position_form, is_create):
    position = position_form.save(commit=False)
    if is_create:
        position.created_by = request.user
    position.last_updated_by = request.user
    position.save()

    grade_level_list = request.POST.getlist('grade_level')

    #https://stackoverflow.com/questions/10691359/django-1-4-bulk-create-with-a-list
    #bulk create
    position_grade_level_list = [PositionGradeLevel(grade_level=grade_level_,
                position=position) for grade_level_ in grade_level_list ]
    PositionGradeLevel.objects.bulk_create(position_grade_level_list)

def create_position_ajax(request, *args, **kwargs):
    data = dict()
    context = dict()

    if request.method == 'POST':
        position_form = forms.PositionForm(data=request.POST)
        if position_form.is_valid():
            is_create = True
            process_post_request(request, position_form, is_create)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        position_form = forms.PositionForm()

    context['mode'] = 'create'
    context['form'] = position_form
    context['object_name'] = 'position'
    data['html_form'] = render_to_string(
        'registration/partial_position_form_ajax.html',
        context,
        request=request
    )
    return JsonResponse(data)

def update_position_ajax(request, pk):
    data = dict()
    context = dict()
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        position_form = forms.PositionForm(request.POST, instance=position)
        if position_form.is_valid():
            is_create = False
            #clear the grade_level on PositionGradeLevel table
            position.grade_levels.all().delete()
            process_post_request(request, position_form, is_create)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        position_form = forms.PositionForm(instance=position)

    context['mode'] = 'update'
    context['form'] = position_form
    context['object_name'] = 'position'
    data['html_form'] = render_to_string(
        'registration/partial_position_form_ajax.html',
        context,
        request=request
    )
    return JsonResponse(data)

def toggle_position_status_ajax(request,pk):
    data = toggle_object_status(object=Position, pk=pk)
    return JsonResponse(data)

def show_more_details_ajax(request, pk):
    data = dict()
    context = dict()
    position = get_object_or_404(Position, pk=pk)
    form = forms.PositionFormMoreDetails(instance=position)

    context['mode'] = 'view'
    context['form'] = form
    context['object_name'] = 'position'
    data['html_form'] = render_to_string(
        'registration/partial_position_form_ajax.html',
        context,
        request=request
    )
    return JsonResponse(data)
