from django.views.generic.edit import CreateView
from django.urls import reverse_lazy,reverse
from registration.models import Student
from registration import forms

class StudentCreate(CreateView):
    model = Student
    fields  = [ 'lrn', 'last_name', 'first_name', 'middle_name', 'sex', 'birth_date', 'age', 'mother_tongue', 'ethnic_group', 'religion', 'address_house_no', 'address_barangay', 'address_municipality', 'address_province', 'father_name', 'mother_name', 'guardian_name', 'guardian_relationship', 'parent_guardian_contact_no', 'remarks', 'classes']  #[f.name for f in RegistrationModels.Student._meta.get_fields()]
    success_url = reverse_lazy('registration:list_student')

    def post(self, request, **kwargs):
        if 'add_more_button' in request.POST:
            self.success_url = reverse_lazy('registration:add_student')
        return super().post(request, **kwargs)
