
from registration.viewsF.cbv import create_user
from django.contrib.auth.models import User, Group
from registration.models import ElectionOfficer
from registration import forms
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def update_user_ajax(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        #if post, set the form the instance of the user
        user_form =  forms.UserForm(request.POST, instance=user)
    else:
        user_form = forms.UserForm(instance=user)

    #get user groups
    groups = Group.objects.order_by('name').filter(user=user).values_list('name',flat=True)

    #check if user is/was an election Officer
    if ElectionOfficer.objects.filter(user=user).first():
        election_officer_flag = True
    else:
        election_officer_flag = False

    #reuse the function view from creatue_user.py
    return create_user.create_user_ajax(request, election_officer_flag=election_officer_flag, groups=groups, user_form=user_form, template='registration/partial_user_update_ajax.html')

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
