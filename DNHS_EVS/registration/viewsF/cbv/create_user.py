from django.views.generic import TemplateView
from django.urls import reverse_lazy,reverse
from registration import forms
from django.contrib.auth.forms import UserCreationForm
from registration.models import UserProfile,Student,ElectionOfficer
from django.contrib.auth.models import User,Group
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string

class UserCreate(TemplateView):
    template_name = 'registration/user_create.html'
    mode = "create user" #default, but set during the call on urls.py

    def processing_post_request(self, request, **kwargs):
        data = dict()
        if 'user_form' in kwargs:
            #from update user
            user_form = kwargs.get("user_form")
        else:
            user_form  = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            #check if for_student checkbox is checkbox
            for_student = user_form.cleaned_data['for_student']
            # print("Student LRN: " + str(user_form.cleaned_data['student_lrn']))
            print("Student LRN: " + str(request.POST))

            if for_student:
                #put a mechanism to check if user has already a record in election_officer table
                #even if lrn is not checked. 
                student = Student.objects.get(lrn=user_form.cleaned_data['student_lrn'])
                profile.student = student

                #if for election_officer
                if for_student[0] == 'election_officer':
                    election_officer, created = ElectionOfficer.objects.get_or_create(
                        student = student,
                        user = user,
                    )
                    # election_officer.student = student
                    election_officer.is_active = True
                    election_officer.save()
                    #add user to group
                    group = Group.objects.get(name="Election Officer")
                    group.user_set.add(user)
            else: #try to revoke privilege for election officer
                #check if election Officer exist
                election_officer = ElectionOfficer.objects.filter(pk=user).first()
                if election_officer:
                    #deactivate election_officer
                    election_officer.is_active = False
                    election_officer.save()

                #remove from Election Officer group
                try:
                    election_officer_group = Group.objects.get(name="Election Officer")
                    election_officer_group.user_set.remove(user)
                except:
                    pass

            #check if other groups are checked
            other_groups = user_form.cleaned_data['other_groups']
            if other_groups:
                if 'teacher' in other_groups:
                    group = Group.objects.get(name="Teacher")
                    try:
                        group.user_set.add(user)
                    except:
                        pass
                else: #revoke teacher
                    try:
                        group = Group.objects.get(name="Teacher")
                        group.user_set.remove(user)
                    except:
                        pass

                if 'system_administrator' in other_groups:
                    group = Group.objects.get(name="System Administrator")
                    try:
                        group.user_set.add(user)
                    except:
                        pass
                else: #revoke System Administrator
                    try:
                        group = Group.objects.get(name="System Administrator")
                        group.user_set.remove(user)
                    except:
                        pass
            else: #revoke Teacher and System Administrator Group
                try:
                    group = Group.objects.get(name="Teacher")
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name="System Administrator")
                    group.user_set.remove(user)
                except:
                    pass

            profile.save()
            data['form_is_valid'] = True

        else:
            data['form_is_valid'] = False
            print (user_form.errors,profile_form.errors)
        data['user_form'] = user_form
        data['profile_form'] = profile_form
        return data

    def get(self, request):
        student_list = Student.objects.all()
        user_form = forms.UserForm()
        profile_form = forms.UserProfileForm()
        # mode = "create user"
        return render (request,self.template_name,
                        {
                            'user_form': user_form,
                            'profile_form': profile_form,
                            'student_list': student_list,
                            'mode': self.mode,
                        }
                        )

    def post(self, request, **kwargs):
        self.processing_post_request(request, **kwargs)
        return  HttpResponseRedirect(reverse('registration:list_user'))


##################
def validate_username(request):  #responsible for ajax request
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'This Username already exist!'
    return JsonResponse(data)

def create_user_ajax(request, **kwargs):
    data = dict()
    context = dict()

    if request.method == 'POST':
        user_create = UserCreate()
        data = user_create.processing_post_request(request, **kwargs)
        context['user_form'] = data['user_form']
        #delete to prevent error while serializing
        try:
            del data['user_form']
            del data['profile_form']
        except:
            pass
    else:
        if 'user_form' in kwargs:
            context['user_form'] = kwargs.get('user_form')
        else:
            context['user_form'] = forms.UserForm()

    if 'template' in kwargs: #from update_user
        template = kwargs['template']
    else: #default template if not set
        template = 'registration/partial_user_create_ajax.html'

    if 'groups' in kwargs: #from update_user
        context['groups'] = kwargs.get('groups')

    student_list = Student.objects.all()
    context['student_list'] = student_list
    data['html_form'] = render_to_string(template,
                context,
                request=request,
                )
    return JsonResponse(data)
