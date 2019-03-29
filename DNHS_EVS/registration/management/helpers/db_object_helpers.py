from django.shortcuts import get_object_or_404
from registration.models_election import Position
from registration.models import Student
from collections import namedtuple
from django.db import connection
import itertools

class DatabaseObjectHelps():
    pass

def get_student_summary_data(*args, **kwargs):
    '''
        get the student summary data given filter specied.
        Return a namedtuple
    '''
    election = kwargs.get('election', None)
    # print(**kwargs)
    if election:
        school_year = election.school_year
        grade_levels = [ [grade_level.grade_level for grade_level in position.grade_levels.all()] \
                   for position in election.positions.all()
                ]
        #https://stackoverflow.com/questions/716477/join-list-of-lists-in-python
        grade_levels = set(list(itertools.chain.from_iterable(grade_levels))) #merge all items and remove duplicates

        print(grade_levels)
        sql_query = "select grade_level, section, sex, count(*) \
                    from registration_student a , registration_student_classes b, \
                        registration_class c, registration_sex d \
                    where a.id = b.student_id and a.sex_id = d.id	\
                        and b.class_id = c.id and c.school_year = '%s' \
                        and c.grade_level in (%s)    \
                    group by grade_level, section, sex order by grade_level, section" \
                    % (school_year,
                    ", ".join( "'{}'".format(grade_level) for grade_level in grade_levels)
                    #to convery the set into a usable sql for in statement
                    )

    else:
        sql_query = "select grade_level, section, sex, count(*) \
                    from registration_student a , registration_student_classes b, \
                        registration_class c, registration_sex d \
                    where a.id = b.student_id and a.sex_id = d.id	\
                        and b.class_id = c.id  \
                    group by grade_level, section, sex order by grade_level, section"

    #https://django.readthedocs.io/en/2.1.x/topics/db/sql.html

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        desc = cursor.description
        namedtuple_result = namedtuple('Summary',[col[0] for col in desc])
        return [namedtuple_result(*row) for row in cursor.fetchall()]


def toggle_object_status(*args, **kwargs):
    '''
        This will toggle the status of the given object from active to inactive
        and via versa.
    '''
    return_data = dict()
    Object = kwargs.get('object', None)
    pk = kwargs.get('pk',None)
    if Object and pk:
        if Object.__name__ in ['Position','Party','Election','Candidate']:
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
