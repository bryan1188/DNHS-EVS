from django.views.generic import TemplateView,DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from registration import forms
from registration.models import Election,Student,Class,Sex
from registration.management.helpers.db_object_helpers import toggle_object_status
from registration.management.helpers.db_object_helpers import get_student_summary_data
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
        #get summary

        return context

class ElectionDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'registration.add_election'
    template_name = 'registration/election_detail.html'
    model = Election

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.ElectionForm(instance = self.object)
        filter_form = forms.GenericFilterForm()
        context['filter_form'] = filter_form
        context['form'] = form
        context['modal_ajax_location'] = settings.MODAL_AJAX_LOCATION
        return context

@permission_required('registration.add_election', raise_exception=True)
def populate_table_election_list_ajax(request):
    select_all = request.GET.get('select_all')
    school_year = request.GET.get('school_year', None)
    if school_year:
        if select_all == "true":
            election_list = Election.all_objects.filter(school_year__iexact = school_year)
        else:
            election_list = Election.objects.filter(
                        school_year__iexact = school_year
                        )
    else:
        if select_all == "true":
            election_list = Election.all_objects.all()
        else:
            election_list = Election.objects.all()
    json = serializers.serialize('json', election_list)
    return HttpResponse(json, content_type='application/json')

@permission_required('registration.add_election', raise_exception=True)
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

@permission_required('registration.add_election', raise_exception=True)
def update_election_ajax(request, pk):
    data = dict()
    context = dict()
    election = get_object_or_404(Election.all_objects.all(), pk=pk)
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

@permission_required('registration.add_election', raise_exception=True)
def toggle_election_status_ajax(request,pk):
    data = toggle_object_status(object=Election, pk=pk)
    return JsonResponse(data)

@permission_required('registration.add_election', raise_exception=True)
def show_more_details_ajax(request, pk):
    data = dict()
    context =  dict()
    position = get_object_or_404(Election.all_objects.all(), pk = pk)
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

@permission_required('registration.add_election', raise_exception=True)
def populate_table_voters_list_ajax(request, election_id):
    student_list = []
    election = Election.objects.get(id = election_id)
    school_year = election.school_year
    grade_level = set()
    for position in election.positions.all(): #get the list of grade level
        for grade_level_ in position.grade_levels.all():
            grade_level.add(grade_level_.grade_level)
    class_list = Class.objects.filter(school_year=school_year,
                    grade_level__in=grade_level)
    for class_ in class_list:
        for student in class_.students.all():
            student_json = {}
            student_ = {}
            student_['name'] = student.__str__()
            student_['sex'] = student.sex.__str__()
            student_['grade_level'] = class_.grade_level
            student_['section'] = class_.section
            student_json['pk'] = student.id
            student_json['fields'] = student_
            student_list.append(student_json)

    return HttpResponse(json.dumps(student_list), content_type='application/json')

@permission_required('registration.add_election', raise_exception=True)
def populate_table_voters_summary_ajax(request, election_id):
    # return_list = []
    # election = Election.objects.get(id = election_id)
    # school_year = election.school_year
    # for position in election.positions.all(): #get summary
    #     for grade_level in position.grade_levels.all():
    #         class_list = Class.objects.filter(grade_level = grade_level.grade_level)
    #         for class_ in class_list:
    #             row = {}
    #             section = class_.section
    #             row['grade_level'] = grade_level.grade_level
    #             row['section'] = section
    #             row['male_count'] = Sex.objects.get(
    #                     sex='M').students.filter(
    #                     classes__school_year=school_year,
    #                     classes__grade_level=grade_level,
    #                     classes__section=section).count()
    #             row['female_count'] = Sex.objects.get(
    #                     sex='F').students.filter(
    #                     classes__school_year=school_year,
    #                     classes__grade_level=grade_level.grade_level,
    #                     classes__section=section).count()
    #             if not (row['male_count'] == 0 and row['female_count'] == 0) :
    #                 return_list.append(row)
    return_dict = dict()
    return_list_rows = []
    return_dict_summary = dict()
    return_dict_summary['female_count'] = 0
    return_dict_summary['male_count'] = 0
    return_dict_summary['grand_total'] = 0
    row_counter = 1
    summary = get_student_summary_data(election = Election.objects.get(id = election_id))
    for row in summary:
        if row_counter % 2 != 0: # new section, create new row
            row_json_cleaned = {}
            row_json_cleaned['grade_level'] = row.grade_level
            row_json_cleaned['section'] = row.section
        if row.sex == "F":
            row_json_cleaned['female_count'] = row.count
            return_dict_summary['female_count'] += row.count
        else:
            row_json_cleaned['male_count'] = row.count
            return_dict_summary['male_count'] += row.count
        return_dict_summary['grand_total'] += row.count
        if row_counter % 2 == 0:
            row_json_cleaned['total'] = row_json_cleaned['male_count'] + row_json_cleaned['female_count']
            return_list_rows.append(row_json_cleaned)
        row_counter += 1
    return_dict['rows'] = return_list_rows
    return_dict['summary'] = return_dict_summary

    return HttpResponse(json.dumps(return_dict), content_type='application/json')
