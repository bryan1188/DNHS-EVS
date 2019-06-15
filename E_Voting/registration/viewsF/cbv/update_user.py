from django.views.generic.edit import UpdateView
from django.urls import reverse,reverse_lazy
from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect


class UserUpdateView(UpdateView):
    fields  = [ 'username','password','is_active','last_name','first_name']
    model = User
    success_url = reverse_lazy('registration:update_user')
    template_name = 'registration/user_create.html'
