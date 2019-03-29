from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from DNHS_EVS import views as MainViews
from registration.viewsF.cbv import (
                    upload_students,update_student,
                    list_student,create_student,delete_student,create_user,
                    list_user,election,position,party,candidate
)
from registration.viewsF.functionBV import update_user

app_name = 'registration'

urlpatterns = [
    path('',MainViews.HomePage.as_view(),name='home'),
    path('uploadstudents/',upload_students.UploadStudents.as_view(),
        name='upload_students'
        ),
    path('uploadstudents/verification/',
        upload_students.UploadStudentsVerification.as_view(),
        name='upload_students_verification'
        ),
    path('students/',list_student.StudentsListView.as_view(),
        name='list_student'
        ),
    url(r'^student/update/(?P<pk>\d+)/',
        update_student.StudentUpdateView.as_view(),
        name='update_student'
        ),
    path('student/add/',create_student.StudentCreate.as_view(),
        name='add_student'
        ),
    url(r'^student/delete/(?P<pk>\d+)/',
        delete_student.StudentDelete.as_view(),
        name='delete_student'
        ),
    path('user/create/', create_user.UserCreate.as_view(mode="create user"),
        name='create_user'
        ),
    path('ajax/user/update/<int:pk>/',
        update_user.update_user_ajax,
        name='update_user_ajax'
        ),
    path('ajax/user/reset_password/<int:pk>/',
        update_user.update_user_reset_password_ajax,
        name='update_user_reset_password_ajax'
        ),
    path('ajax/user/deactivate_activate/<int:pk>/',
        update_user.deactivate_activate_ajax,
        name='deactivate_activate_ajax'
        ),
    path('users/',
        list_user.UserList.as_view(),
        name='list_user'
        ),
    path('ajax/user/create/',
        create_user.create_user_ajax,
        name='create_user_ajax'
        ),
    path('election_officer/create/',
        create_user.UserCreate.as_view(mode="create election officer"),
        name='create_election_officer'
        ),
    path('ajax/validate_username/',
        create_user.validate_username,
        name='validate_username_ajax'),
    path('ajax/get_filter_options_for_level/',
        list_student.get_filter_options_for_level,
        name='get_filter_options_for_level_ajax'
        ),
    path('ajax/populate_table_upladed_students/',
        list_student.populate_table_upladed_students,
        name='populate_table_upladed_students_ajax'
        ),
    path('ajax/populate_table_uploaded_students_2/',
        list_student.populate_table_uploaded_students_2,
        name='populate_table_uploaded_students_2_ajax'
        ),
    path('ajax/get_filter_options_for_section/',
        list_student.get_filter_options_for_section,
        name='get_filter_options_for_section_ajax'
        ),
    path('ajax/user/populate_table_user_list_ajax/',
        list_user.populate_table_user_list_ajax,
        name='populate_table_user_list_ajax'
        ),
    path('elections/', election.ElectionList.as_view(),name='list_election'),
    path('election/<int:pk>/',
        election.ElectionDetail.as_view(),
        name='detail_election'
        ),
    path('ajax/elections/populate_table_election_list_ajax/',
        election.populate_table_election_list_ajax,
        name='populate_table_election_list_ajax'
        ),
    path('ajax/election/ceate/', election.create_election_ajax,
        name='create_election_ajax'
        ),
    path('ajax/election/update/<int:pk>/',
        election.update_election_ajax,
        name='update_election_ajax'
        ),
    path('ajax/election/toggle_status/<int:pk>/',
        election.toggle_election_status_ajax,
        name='toggle_election_status_ajax'
    ),
    path('ajax/election/more_details/<int:pk>/',
        election.show_more_details_ajax,
        name='election_show_more_details_ajax'
    ),
    path('ajax/election/populate_table_voters_list_ajax/<int:election_id>/',
        election.populate_table_voters_list_ajax,
        name='populate_table_voters_list_ajax'
        ),
    path('ajax/election/populate_table_voters_summary_ajax/<int:election_id>/',
        election.populate_table_voters_summary_ajax,
        name='populate_table_voters_summary_ajax'
        ),
    path('positions/', position.PositionList.as_view(), name='position'),
    path('ajax/positions/populate_table_election_list_ajax/',
        position.populate_table_position_list_ajax,
        name='populate_table_position_list_ajax'
    ),
    path('ajax/position/create/', position.create_position_ajax,
        name='create_position_ajax'
    ),
    path('ajax/position/update/<int:pk>/',
        position.update_position_ajax,
        name='update_position_ajax'
    ),
    path('ajax/position/toggle_status/<int:pk>/',
        position.toggle_position_status_ajax,
        name='toggle_position_status_ajax'
    ),
    path('ajax/position/more_details/<int:pk>/',
        position.show_more_details_ajax,
        name='show_more_details_ajax'
    ),
    path('parties/', party.PartyList.as_view(), name='party'),
    path('ajax/parties/populate_table_party_list_ajax/',
        party.populate_table_party_list_ajax,
        name='populate_table_party_list_ajax'
        ),
    path('ajax/party/create/', party.create_ajax,
        name='create_party_ajax'
    ),
    path('ajax/party/update/<int:pk>/',
        party.update_ajax,
        name='update_party_ajax'
    ),
    path('ajax/party/more_details/<int:pk>/',
        party.show_more_details_ajax,
        name='part_more_details_ajax'
    ),
    path('ajax/party/toggle_status/<int:pk>/',
        party.toggle_status_ajax,
        name='party_toggle_status_ajax'
    ),
    path('candidates/', candidate.CandidateList.as_view(), name='candidate'),
    path('ajax/candidates/populate_table_candidate_list_ajax/',
        candidate.populate_table_list_ajax,
        name='populate_table_candidate_list_ajax'
        ),
    path('ajax/candidate/create/', candidate.create_ajax,
        name='create_candidate_ajax'
    ),
    path('ajax/candidate/populate_options_for_student/',
        candidate.populate_options_for_student_ajax,
        name='candidate_populate_options_for_student_ajax'
        ),
    path('ajax/candidate/update/<int:pk>/',
        candidate.update_ajax,
        name='candidate_update_ajax'
    ),
    path('ajax/candidate/toggle_status/<int:pk>/',
        candidate.toggle_status_ajax,
        name='candidate_toggle_status_ajax'
    ),
    path('ajax/candidate/more_details/<int:pk>/',
        candidate.show_more_details_ajax,
        name='candidate_more_details_ajax'
    ),
]
