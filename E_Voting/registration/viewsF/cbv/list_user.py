from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from registration import forms
from django.contrib.auth.models import User,Group
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
import json

class UserList(PermissionRequiredMixin,TemplateView):
    template_name = 'registration/user_list.html'
    permission_required = 'auth.add_user'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_filter_form = forms.UserFilterForm()
        context['user_filter_form'] = user_filter_form
        context['modal_ajax_location'] = settings.MODAL_AJAX_LOCATION
        return context

@permission_required('auth.add_user', raise_exception=True)
def populate_table_user_list_ajax(request):
    selected_group = request.GET.getlist('group[]')
    active = request.GET.get('is_active')
    select_all_users = request.GET.get('select_all_users')
    if selected_group:
        user_list = User.objects.filter(groups__name__in=selected_group)
    else:
        user_list = User.objects.exclude(groups__name__isnull=True)

    if active == "true":
        user_list = user_list.filter(is_active=True)
    else:
        user_list = user_list.filter(is_active=False)

    if select_all_users == "true":
        user_list = User.objects.all()

    user_list = user_list.distinct('username')

    return_list = []
    for user in user_list:
        user_json = {}
        user_ = {}
        user_['username'] = user.username
        user_['first_name'] = user.first_name
        user_['last_name'] = user.last_name
        user_['is_active'] = user.is_active
        user_['pk'] = user.id
        if user.groups.count() < 1:
            user_['groups'] = ""
        else:
            groups = Group.objects.order_by('name').filter(user=user).values_list('name',flat=True)
            user_['groups'] = [group for group in groups]
        user_json['pk'] = user.id
        user_json['fields'] = user_
        return_list.append(user_json)

    return HttpResponse (json.dumps(return_list),content_type='application/json')
