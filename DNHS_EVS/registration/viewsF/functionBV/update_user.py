
from registration.viewsF.cbv import create_user
from django.contrib.auth.models import User, Group
from registration.models import ElectionOfficer, UserProfile
from registration import forms
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

def update_user_ajax(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_form =  forms.UserFormUpdate(request.POST, instance=user)
    else:
        user_form = forms.UserFormUpdate(instance=user)

    #get user groups
    groups = Group.objects.order_by('name').filter(user=user).values_list('name',flat=True)

    #check if user is/was an election Officer
    if ElectionOfficer.objects.filter(user=user).first():
        election_officer_flag = True
    else:
        election_officer_flag = False

    #reuse the function view from creatue_user.py
    return create_user.create_user_ajax(request, election_officer_flag=election_officer_flag, \
            groups=groups, user_form=user_form, template='registration/partial_user_update_ajax.html')

def update_user_reset_password_ajax(request,pk):
    context = dict()
    data = dict()
    user = get_object_or_404(User,pk=pk)

    if request.method == 'POST':
        user_form =  forms.UserFormUpdatePassword(request.POST, instance=user)
        if user_form.is_valid():
            profile = UserProfile(user=user)
            profile.password_is_temp = True
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        user_form =  forms.UserFormUpdatePassword(instance=user)

    context['user_form'] = user_form
    context['user'] = user
    data['html_form'] = render_to_string('registration/partial_user_update_password_ajax.html',
                context,
                request=request,
                )
    return JsonResponse(data)

def deactivate_activate_ajax(request, pk):
    user = get_object_or_404(User, pk=pk)
    data = dict()
    if (user.is_active):
        user.is_active = False
        data['message'] = 'User Deactivated!'
    else:
        user.is_active = True
        data['message'] = 'User Activated!'
    user.save()

    return JsonResponse(data)
