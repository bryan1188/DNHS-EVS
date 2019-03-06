
from registration.viewsF.cbv import create_user
from django.contrib.auth.models import User, Group
from registration import forms
from django.shortcuts import get_object_or_404

def update_user_ajax(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        #if post, set the form the instance of the user
        user_form =  forms.UserForm(request.POST, instance=user)
    else:
        user_form = forms.UserForm(instance=user)

    #get user groups
    groups = Group.objects.order_by('name').filter(user=user).values_list('name',flat=True)
    #reuse the function view from creatue_user.py
    return create_user.create_user_ajax(request, groups=groups, user_form=user_form, template='registration/partial_user_update_ajax.html')
