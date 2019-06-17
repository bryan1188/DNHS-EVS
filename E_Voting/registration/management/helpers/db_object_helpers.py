from django.shortcuts import get_object_or_404
from registration.models_election import Position
from registration.models import Student
from collections import namedtuple
from django.db import connection
import itertools

class DatabaseObjectHelps():
    pass

def create_sql_query(**kwargs):
    school_year = kwargs.get('school_year', None)
    grade_levels = kwargs.get('grade_levels', None)
    sections = kwargs.get('sections', None)
    student_ids = kwargs.get('student_ids', None)
    school_year_student_ids = kwargs.get('school_year_student_ids', None)
    sql_query = ""

    if sections:
        sql_query = "select grade_level,grade_level_integer, section, sex, count(*) \
                    from registration_student a , registration_student_classes b, \
                        registration_class c, registration_sex d \
                    where a.id = b.student_id and a.sex_id = d.id	\
                        and b.class_id = c.id and c.school_year = '%s' \
                        and c.section in (%s)                \
                    group by grade_level, grade_level_integer, section, sex \
                    order by grade_level_integer, section" \
                    % (school_year,
                    ", ".join( "'{}'".format(section) for section in sections)
                    #to convery the set into a usable sql for in statement
                    )
    elif grade_levels:
        sql_query = "select grade_level,grade_level_integer, section, sex, count(*) \
                    from registration_student a , registration_student_classes b, \
                        registration_class c, registration_sex d \
                    where a.id = b.student_id and a.sex_id = d.id	\
                        and b.class_id = c.id and c.school_year = '%s' \
                        and c.grade_level in (%s)    \
                    group by grade_level, grade_level_integer, section, sex \
                    order by grade_level_integer, section" \
                    % (school_year,
                    ", ".join( "'{}'".format(grade_level) for grade_level in grade_levels)
                    #to convery the set into a usable sql for in statement
                    )
    elif student_ids:
        sql_query = "select grade_level,grade_level_integer, section, sex, count(*) \
                    from registration_student a , registration_student_classes b, \
                        registration_class c, registration_sex d \
                    where a.id = b.student_id and a.sex_id = d.id	\
                        and b.class_id = c.id  and c.school_year = '%s' \
                        and a.id in (%s)                \
                    group by grade_level, grade_level_integer, section, sex \
                    order by grade_level_integer, section" \
                    % (school_year_student_ids, ", ".join( "'{}'".format(student_id) for student_id in student_ids)
                    #to convery the set into a usable sql for in statement
                    )
    else:
        sql_query = "select grade_level,grade_level_integer, section, sex, count(*) \
                    from registration_student a , registration_student_classes b, \
                        registration_class c, registration_sex d \
                    where a.id = b.student_id and a.sex_id = d.id	\
                        and b.class_id = c.id and c.school_year = '%s' \
                    group by grade_level, grade_level_integer, section, sex \
                    order by grade_level_integer, section" \
                    % (school_year)

    return sql_query

def get_student_summary_data(*args, **kwargs):
    '''
        get the student summary data given filter specied.
        Return a namedtuple
    '''
    election = kwargs.get('election', None)
    #used for student List
    school_year_p = kwargs.get('school_year', None)
    grade_levels_p = kwargs.get('grade_levels', None)
    sections_p = kwargs.get('sections', None)
    student_ids = kwargs.get('student_ids', None)
    school_year_student_ids = kwargs.get('school_year_student_ids', None)
    if election:
        school_year = election.school_year
        grade_levels = [ [grade_level.grade_level for grade_level in position.grade_levels.all()] \
                   for position in election.positions.all()
                ]
        #https://stackoverflow.com/questions/716477/join-list-of-lists-in-python
        grade_levels = set(list(itertools.chain.from_iterable(grade_levels))) #merge all items and remove duplicates
        sql_query = create_sql_query(
                        school_year=school_year,
                        grade_levels=grade_levels
        )
    elif school_year_p:
        if sections_p:
            if isinstance(sections_p, list):
                sections_p = set(sections_p)
            else:
                sections_p = {sections_p}
            sql_query = create_sql_query(
                            school_year=school_year_p,
                            sections = sections_p
            )
        elif grade_levels_p:
            if isinstance(grade_levels_p, list):
                grade_levels_p = set(grade_levels_p)
            else:
                grade_levels_p = {grade_levels_p}
            sql_query = create_sql_query(
                            school_year=school_year_p,
                            grade_levels = grade_levels_p
            )
        else:
            sql_query = create_sql_query(
                            school_year=school_year_p
            )
    elif student_ids:
        if isinstance(student_ids, list):
            student_ids = set(student_ids)
        else:
            student_ids = {student_ids}
        sql_query = create_sql_query(
                    student_ids=student_ids,
                    school_year_student_ids=school_year_student_ids
        )
    else:
        sql_query = "select grade_level,grade_level_integer, section, sex, count(*) \
                    from registration_student a , registration_student_classes b, \
                        registration_class c, registration_sex d \
                    where a.id = b.student_id and a.sex_id = d.id	\
                        and b.class_id = c.id  \
                    group by grade_level, grade_level_integer, section, sex \
                    order by grade_level_integer, section"

    #https://django.readthedocs.io/en/2.1.x/topics/db/sql.html
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        desc = cursor.description
        namedtuple_result = namedtuple('Summary',[col[0] for col in desc])
        return [namedtuple_result(*row) for row in cursor.fetchall()]

def live_monitoring_participation_rate(**kwargs):
    '''
        get the participation rate data by grade level or by section
        return data is list of dictionary
            by_ident:
            number of voters:
            number of voters casted:
            participation rate:
    '''
    election_id = kwargs.get('election_id')
    by_grade_level_or_section = kwargs.get('by_identifier')

    sql_query = "\
            select {by_identifier}, is_vote_casted, count(*)\
            from django.registration_voter voter,\
            	django.registration_student student, \
            	django.registration_class class \
            where voter.student_id = student.id \
            	and voter.student_class_id = class.id \
            	and voter.election_id = {election_id} \
            group by {by_identifier}, is_vote_casted,grade_level_integer \
            order by grade_level_integer	\
           ".format(
                by_identifier = by_grade_level_or_section,
                election_id = election_id
           )
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        desc = cursor.description
        namedtuple_result = namedtuple('Summary',[col[0] for col in desc])
        namedtuple_result =  [namedtuple_result(*row) for row in cursor.fetchall()]

        # use the return named tuple instead of querying in the database to improve performance
        #create return list dictionary
        return_list =  list()
        item_dictionary = dict()

        #build the list of grade_level/section
        grade_level_section = list()
        for item in namedtuple_result:
            if item[0] not in grade_level_section:
                grade_level_section.append(item[0])

        for item in grade_level_section:
            number_of_voters = sum([row.count for row in namedtuple_result if row[0]==item])
            number_of_voters_voted = sum([row.count for row in namedtuple_result \
                                        if row[0]==item if row.is_vote_casted])
            item_dictionary = dict()
            item_dictionary['grade_level_or_section'] = item
            item_dictionary['number_of_voters'] = number_of_voters
            item_dictionary['number_of_voters_voted'] = number_of_voters_voted
            item_dictionary['number_of_voters_not_voted'] = number_of_voters - number_of_voters_voted
            item_dictionary['participation_rate'] = round((number_of_voters_voted/number_of_voters) * 100, 2)
            return_list.append(item_dictionary)
        return return_list

def truncate_table(table_object):
    '''
        this will do truncate. not delete.
        Used for tables that has high security like Vote
    '''
    table_name = table_object._meta.db_table
    sql_query = "truncate table {}".format(table_name)
    with connection.cursor() as cursor:
        cursor.execute(sql_query)

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
