from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from DNHS_EVS import views as MainViews
from registration.viewsF.cbv import upload_students,update_student,list_student,create_student,delete_student,create_user,list_user
from registration.viewsF.functionBV import update_user

app_name = 'registration'

urlpatterns = [
    path('',MainViews.HomePage.as_view(),name='home'),
    path('uploadstudents/',upload_students.UploadStudents.as_view(),name='upload_students'),
    path('uploadstudents/verification/',upload_students.UploadStudentsVerification.as_view(),name='upload_students_verification'),
    path('students/',list_student.StudentsListView.as_view(), name='list_student'),
    url(r'^student/update/(?P<pk>\d+)/',update_student.StudentUpdateView.as_view(), name='update_student'),
    path('student/add/',create_student.StudentCreate.as_view(), name='add_student'),
    url(r'^student/delete/(?P<pk>\d+)/',delete_student.StudentDelete.as_view(), name='delete_student'),
    path('user/create/', create_user.UserCreate.as_view(mode="create user"), name='create_user'),
    url(r'^user/update/(?P<pk>\d+)/',update_user.update_user_ajax, name='update_user'),
    # path('user/update/<init:pk>/', create_user.UserCreate.as_view(mode="create user"), name='create_user'),
    path('users/', list_user.UserList.as_view(), name='list_user'),
    path('ajax/user/create/', create_user.create_user_ajax, name='create_user_ajax'),
    path('election_officer/create/', create_user.UserCreate.as_view(mode="create election officer"), name='create_election_officer'),
    path('ajax/validate_username/', create_user.validate_username, name='validate_username_ajax'),
    path('ajax/get_filter_options_for_level/', list_student.get_filter_options_for_level, name='get_filter_options_for_level_ajax'),
    path('ajax/populate_table_upladed_students/', list_student.populate_table_upladed_students, name='populate_table_upladed_students_ajax'),
    path('ajax/populate_table_uploaded_students_2/', list_student.populate_table_uploaded_students_2, name='populate_table_uploaded_students_2_ajax'),
    path('ajax/get_filter_options_for_section/', list_student.get_filter_options_for_section, name='get_filter_options_for_section_ajax'),
    path('ajax/user/populate_table_user_list_ajax/', list_user.populate_table_user_list_ajax, name='populate_table_user_list_ajax'),
]
