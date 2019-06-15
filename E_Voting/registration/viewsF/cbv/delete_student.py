from django.urls import reverse
from django.views.generic.edit import DeleteView
from registration.models import Student

class StudentDelete(DeleteView):
    model = Student

    def get_success_url(self):
        return  reverse(self.request.session.get('update_student_prev_url','registration:list_student'))
