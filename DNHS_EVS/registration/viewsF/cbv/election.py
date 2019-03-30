from django.views.generic import TemplateView,DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from registration import forms
from registration.models import Election,Student,Class,Sex,Candidate,Voter
from registration.management.helpers.db_object_helpers import toggle_object_status
from registration.management.helpers.db_object_helpers import get_student_summary_data
from registration.management.helpers.token_generator import BatchKeyGenerator
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

def get_voters_list(election_id): #permission not required since this is internal def
    '''
        return student_list of all voters based on the given election_id
    '''
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
            student_['lrn'] = student.lrn
            student_['sex'] = student.sex.__str__()
            student_['class_id'] = class_.id
            student_['grade_level'] = class_.grade_level
            student_['section'] = class_.section
            student_json['pk'] = student.id
            student_json['fields'] = student_
            student_list.append(student_json)
    return student_list

@permission_required('registration.add_election', raise_exception=True)
def populate_table_voters_list_ajax(request, election_id):
    student_list = get_voters_list(election_id)
    return HttpResponse(json.dumps(student_list), content_type='application/json')

@permission_required('registration.add_election', raise_exception=True)
def populate_table_voters_summary_ajax(request, election_id):
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

@permission_required('registration.add_student', raise_exception=True)
def generate_batch_token_ajax(request, election_id):
    '''
        Generate a token in a batch for a newly created election.
        Make sure that the election.is_token_generated is false before generating
    '''
    batch_key_generator = BatchKeyGenerator(size = 6)
    election = Election.objects.get(id = election_id)
    student_list = get_voters_list(election_id)
    return_list = []
    if not election.is_token_generated:
        for student in student_list:
            student_json = {}
            student_json['pk'] = student['pk']
            student_json['name'] = student['fields']['name']
            student_json['lrn'] = student['fields']['lrn']
            student_json['grade_level']  = student['fields']['grade_level']
            student_json['section']  = student['fields']['section']
            student_json['class_id'] = student['fields']['class_id']
            student_json['election_id'] = election_id
            candidates = Candidate.objects.get_candidate_of_voter(
                                            election,
                                            student_json['grade_level']
                                                    )
            student_json['candidates'] = list(candidates.values('student','position'))
            student_json['token'] = batch_key_generator.generate_key(
                chars = str(student_json['name']) + str(student_json['lrn'] \
                        + str(student_json['grade_level']) + str(student_json['section'])
                )
            )
            student_json['token'] = student_json['token'] + "-{}".format(election_id)
            return_list.append(student_json)

            #insert into database
            candidates = [candidate for candidate in candidates]
            voter = Voter(
                    student = Student.objects.get(id = student_json['pk']),
                    student_class = Class.objects.get( id = student_json['class_id']),
                    election = election,
                    voter_token = student_json['token']
            )
            voter.save()
            voter.candidates.set(candidates)
        #set election.is_token_generated to true
        election.is_token_generated = True
        election.status = "FINALIZED"
        election.save()

    return HttpResponse(json.dumps(return_list), content_type='application/json')

@permission_required('registration.add_student', raise_exception=True)
def populate_voters_token_table_ajax(request, election_id):
    election = Election.objects.get(id = election_id)
    voters = Voter.objects.filter(election=election)
    return_list = []
    for voter in voters:
        voter_json = {}
        voter_json['grade_level'] = voter.student_class.grade_level
        voter_json['section'] = voter.student_class.section
        voter_json['name'] = voter.student.__str__()
        voter_json['sex'] = voter.student.sex.__str__()
        voter_json['token'] = voter.voter_token
        return_list.append(voter_json)
    return HttpResponse(json.dumps(return_list), content_type='application/json')
