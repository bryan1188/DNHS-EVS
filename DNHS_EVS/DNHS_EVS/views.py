from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class HomePage(TemplateView):
    template_name = 'home_page.html'

    def get(self, request, *args, **kwargs):
        # permissions_group =
        return super().get(self)

class TestPage(TemplateView):
    template_name = 'test.html'

class LoginView(LoginView):
    template_name = 'login.html'

class LoginViewAjax(LoginView):
    template_name = 'partial_login_ajax.html.html'

    def get(self, request, *args, **kwargs):
        data = dict()
        context = super().get_context_data(**kwargs)
        data['html_form'] = render_to_string(self.template_name,
                    context,
                    request=request,
                    )
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = dict()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        context = super().get_context_data(**kwargs)
        if user is not None:
            login(request,user)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
        data['html_form'] = render_to_string(self.template_name,
                    context,
                    request=request,
                    )
        return JsonResponse(data)

@login_required
def logout_view_ajax(request):
    data = dict()
    logout(request)
    data['success_status'] = True
    return JsonResponse(data)
