from django.views.generic.edit import UpdateView
from django.urls import reverse,reverse_lazy
from registration import models as RegistrationModels
from django.http import HttpResponseRedirect
# from django.shortcuts import redirect

class StudentUpdateView(UpdateView):
    fields  = [ 'lrn', 'last_name', 'first_name', 'middle_name', 'sex', 'birth_date', 'age', 'mother_tongue', 'ethnic_group', 'religion', 'address_house_no', 'address_barangay', 'address_municipality', 'address_province', 'father_name', 'mother_name', 'guardian_name', 'guardian_relationship', 'parent_guardian_contact_no', 'remarks', 'classes']  #[f.name for f in RegistrationModels.Student._meta.get_fields()]
    model = RegistrationModels.Student
    success_url = reverse_lazy('registration:list_student')

    def get_success_url(self):
        return  reverse(self.request.session.get('update_student_prev_url','registration:list_student'))
        # return redirect(self.request.META.get('HTTP_REFERER')) work on this later

    def post(self, request, **kwargs):
        if 'update_cancel' in request.POST:
            return HttpResponseRedirect(reverse(self.request.session.get('update_student_prev_url','registration:list_student')))
        else:
            return super().post(request, **kwargs)
