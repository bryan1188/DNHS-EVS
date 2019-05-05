
from django.views.generic import TemplateView
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from registration.forms import UploadStudentsForm
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse,reverse_lazy
# from django.conf.urls.static import static
from django.conf import settings
from registration.management.helpers.XlsUploader import XlsUploader
from registration import models
from registration import forms
from registration.management.helpers.db_object_helpers import get_student_summary_data
from registration.viewsF.cbv.election import create_summary_json
from django.http import JsonResponse
import os

class UploadStudentsAjax(PermissionRequiredMixin,View):
    permission_required = 'registration.add_student'

    def get(self, request):
        return render(self.request, 'registration/upload_students.html')

    def post(self,request):
        student_list= []
        data = dict()
        form = UploadStudentsForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        file_path = os.path.join(settings.UPLOAD_DIR,'students','temp')
        if form.is_valid():
            print(files)
            for f in files:
                fs = FileSystemStorage(location=file_path)
                name = fs.save(f.name, f)
                uploader = XlsUploader(file_path="{}/{}".format(file_path,name),index=0) #index 0 means open the first sheet in the workbook.
                uploader.uploadAllData()
                student_list.extend(uploader.student_list)
                fs.delete(name) #delete after upload
            data['student_ids'] = student_list
            data['is_valid'] = True
        else:
            data = {'is_valid': False}
        return JsonResponse(data)



class UploadStudents(PermissionRequiredMixin,FormView):
    form_class = UploadStudentsForm
    template_name = 'registration/upload_students.html'
    success_url = reverse_lazy('registration:list_student')
    permission_required = 'registration.add_student'


    def post(self, request, *args, **kwargs):
        student_list = []
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        file_path = os.path.join(settings.UPLOAD_DIR,'students','temp')
        # self.student_list = [] #list of students uploaded
        if form.is_valid():
            for f in files:
                fs = FileSystemStorage(location=file_path)
                name = fs.save(f.name, f)
                uploader = XlsUploader(file_path="{}/{}".format(file_path,name),index=0) #index 0 means open the first sheet in the workbook.
                uploader.uploadAllData()
                student_list.extend(uploader.student_list)
            students = models.Student.objects.filter(pk__in=student_list)
            # request.session['student_list_pk'] = student_list
            class_filter_form = forms.ClassFilterForm()
            # request.session['update_student_prev_url'] = 'registration:list_student'
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UploadStudentsVerification(TemplateView):
    form_class = UploadStudentsForm
    template_name = 'registration/upload_students_verification.html'

    def get_context_data(self, **kwargs):
        session = self.request.session
        context = super().get_context_data(**kwargs)
        session['update_student_prev_url'] = 'registration:upload_students_verification' #get the prev url. this will be used as success url on update_student.py
        context['student_list'] = list(models.Student.objects.filter(pk__in=session.get('student_list_pk',[])).order_by('last_name','first_name')) #this doesn't work. update the template level for correct ordering. currently it is ordered by lrn
        return context
