from django.shortcuts import get_object_or_404
from registration.models_election import Position

class DatabaseObjectHelps():
    pass

def toggle_object_status(*args, **kwargs):
    return_data = dict()
    Object = kwargs.get('object', None)
    pk = kwargs.get('pk',None)
    if Object and pk:
        if Object.__name__ in ['Position','Party','Election']:
            #special case for position since we are overriding the objects attribute
            object = get_object_or_404(Object.all_objects.all(), pk = pk)
        else:
            object = get_object_or_404(Object, pk = pk)
        try:
            if object.is_active:
                object.is_active = False
                return_data['message'] = 'Object deactivated!'
            else:
                object.is_active = True
                return_data['message'] = 'Object activated!'
            return_data['success_status'] = True
            object.save()
        except:
            return_data['message'] = 'Error while updating the object'
            return_data['success_status'] = False
    else:
        return_data['message'] = 'object or pk is note provided'
        return_data['success_status'] = False
    return return_data
