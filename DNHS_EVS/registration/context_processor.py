from registration.models import School

def set_school_home(request):
    school_name = School.objects.order_by('id').last()
    if not school_name:
        school_name = ""
    else:
        school_name = school_name.name
    return {'school_name':school_name}
