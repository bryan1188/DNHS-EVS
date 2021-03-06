from django.views.generic.list import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from registration import models
from registration import forms
from django.shortcuts import render
from registration.viewsF.cbv.election import create_summary_json
from registration.management.helpers.db_object_helpers import get_student_summary_data
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from django.template.loader import render_to_string
import json
# from django.http import JsonResponse
# import os

# Create your views here.

class StudentsListView(PermissionRequiredMixin, ListView):
    model = models.Student
    permission_required = 'registration.add_student'

    def get_context_data(self, *args, **kwargs):
        session = self.request.session
        context = super().get_context_data(**kwargs)
        session['update_student_prev_url'] = 'registration:list_student' #get the prev url. this will be used as success url on update_student.py
        class_filter_form = forms.ClassFilterForm()
        context['class_filter_form'] = class_filter_form
        context['modal_ajax_location'] = settings.MODAL_AJAX_LOCATION
        return context

@permission_required('registration.add_student', raise_exception=True)
def get_filter_options_for_level(request): # will be called by ajax request
    school_year = request.GET.get('school_year', None)
    classes = models.Class.objects.filter(school_year__iexact=school_year)\
                .order_by('grade_level_integer','grade_level').values('grade_level').distinct('grade_level_integer','grade_level')
    return render(request, 'registration/grade_level_dropdown_list_options.html',{'clasess': classes})

@permission_required('registration.add_student', raise_exception=True)
def get_filter_options_for_section(request): # will be called by ajax request
    grade_level = request.GET.get('grade_level', None)
    school_year = request.GET.get('school_year', None)
    classes = models.Class.objects.filter(grade_level__iexact=grade_level,school_year__iexact=school_year).order_by('section').values('section').distinct('section')
    return render(request, 'registration/section_dropdown_list_options.html',{'clasess': classes})

@permission_required('registration.add_student', raise_exception=True)
def populate_table_upladed_students(request): # will be called by ajax request
    school_year =  request.GET.get('school_year', None)
    grade_level = request.GET.get('grade_level', None)
    section = request.GET.get('section', None)
    student_list = models.Student.objects.filter(classes__school_year=school_year)
    return render(request, 'registration/table_upladed_students.html',
        {'student_list': student_list}
    )

@permission_required('registration.add_student', raise_exception=True)
def populate_table_uploaded_students_2(request): # will be called by ajax request
    school_year =  request.GET.get('school_year', None)
    grade_level = request.GET.get('grade_level', None)
    section = request.GET.get('section', None)
    student_ids = request.GET.getlist('student_ids[]', None) #[] format from front-end
    if student_ids != [''] and student_ids:
        student_list = models.Student.objects.filter(id__in=student_ids)
    else:
        if school_year and grade_level and section: #all filters are available
            student_list = models.Student.objects.filter(classes__school_year=school_year, classes__grade_level=grade_level,classes__section=section)
        elif school_year and grade_level: #school year and grade level filter is available
            student_list = models.Student.objects.filter(classes__school_year=school_year, classes__grade_level=grade_level)
        elif school_year:  #school year
            student_list = models.Student.objects.filter(classes__school_year=school_year)
        else: #no filter
            student_list = models.Student.objects.all() #filter(classes__school_year=school_year)

    #add def natural_key() method on Sex Object
    json = serializers.serialize('json', student_list, use_natural_foreign_keys=True, \
        fields=('id','lrn','last_name','first_name','middle_name','sex','birth_date','age','father_name','mother_name','pk'))
    return HttpResponse(json, content_type='application/json')

@permission_required('registration.add_student', raise_exception=True)
def populate_hmtl_summary_panel_ajax(request):
    data = dict()
    context = dict()
    data['html_form'] = render_to_string(
        'registration/partial_student_list_summary_panel.html',
        context,
        request = request
    )
    return JsonResponse(data)

@permission_required('registration.add_student', raise_exception=True)
def populate_summary_panel_ajax(request):
    school_year =  request.GET.get('school_year', None)
    grade_levels = request.GET.get('grade_level', None)
    sections = request.GET.get('section', None)
    student_ids = request.GET.getlist('student_ids[]', None) #[] format from front-end
    school_year_student_ids = request.GET.get('school_year_student_ids', None)
    if student_ids != [''] and student_ids:
        summary = get_student_summary_data(
                    student_ids=student_ids,
                    school_year_student_ids=school_year_student_ids
        )
    else:
        summary = get_student_summary_data(
                    school_year=school_year,
                    grade_levels=grade_levels,
                    sections=sections
        )
    return_dict = dict()
    return_dict['rows'],return_dict['summary'] = create_summary_json(summary)
    return_dict['panel_html_form'] = render_to_string(
        'registration/partial_student_list_summary_panel.html',
        request = request
    )
    return HttpResponse(json.dumps(return_dict), content_type='application/json')
