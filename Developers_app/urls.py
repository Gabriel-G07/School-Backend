from django.urls import path
from . import views
from .views import *
from django.urls import re_path

urlpatterns = [
    #Signup urls
    path('developers/register/student/', Div_RegisterStudentView.as_view(), name='auth_register_student'),
    path('developers/register/staff/', Div_RegisterStaffView.as_view(), name='auth_register_staff'),
    path('developers/register/teacher/', Div_RegisterTeacherView.as_view(), name='auth_register_teacher'),
    path('developers/parent/register/search/students/', Div_RegisterParentSearchStudentView.as_view(), name='auth_register_parent_search_student'),
    path('developers/register/parent/', Div_RegisterParentView.as_view(), name='auth_register_parent'),
    
    
    #Developer
    path('developer/details/', Div_DetailView.as_view(), name='staff_details'),
    path('developer/dashboard/', Div_DetailView.as_view(), name='staff_details'),
    
    
    
        
    path('developers/staff/', Div_StaffView.as_view(), name='staff'),
    path('developers/students/', Div_StudentsView.as_view(), name='students'),
    path('developers/parents/', Div_ParentsView.as_view(), name='parents'),
    path('developers/staff/job/applications/', Div_JobApplicationsView.as_view(), name='staff_job_applications'),
    path('developers/students/enrolments/', Div_StudentsEnrolmentView.as_view(), name='students_enrolments'),
    path('developers/staff/job/applications/accepted/', Div_AcceptedJobApplicationsView.as_view(), name='staff_job_applications_accepted'),
    path('developers/students/enrolments/accepted/', Div_AcceptedStudentsEnrolmentView.as_view(), name='students_enrolments_accepted'),
    path('developers/admin/fees/search/', Div_SearchStudentView.as_view()),
    path('developers/admin/fees/payment/', Div_MakePaymentView.as_view()),
    path('developers/create-class/', Div_CreateClassView.as_view(), name='create-class'),
    path('developers/teachers/', Div_TeachersView.as_view()),
    path('developers/classes/', Div_ClassesView.as_view()),
    path('developers/enter-campus/', Div_SaveCampusView.as_view()),
    path('developers/campuses/', Div_CampusesView.as_view()),
    
    #Parents
    path('developers/parent/details/', Div_ParentsDetailView.as_view(), name='Parents_details'),
    path('developers/parent/child/details/', Div_ParentsChildDetailsView.as_view(), name='Parents_child_details'),
    path('developers/parent/notices/', Div_ParentsNoticesView.as_view(), name='Parents_noticess'),
    path('developers/parent/classes/', Div_ParentsClassesView.as_view(), name='Parents_classes'),
    path('developers/parent/fees/', Div_ParentsFeesView.as_view(), name='Parents_fees'),
    path('developers/parent/results/', Div_ParentsResultsView.as_view(), name='Parents_results'),
    path('developers/parent/timetables/', Div_ParentsTimeTablessView.as_view(), name='Parents_timetables'),
    path('developers/parent/attendance/', Div_ParentsAttendanceView.as_view()),
    
    
    
    
    #Teachers
    path('developers/classes/primary/students/', Div_TeacherStudentsView.as_view()),
    path('developers/attendance/mark/', Div_MarkAttendanceView.as_view()),
    
    
    
    
    
    
    
    #Students
    path('developers/Student/dashboard/', Div_StudentsDetailView.as_view(), name='Students_details'),
    path('developers/Student/details/', Div_StudentsDetailView.as_view(), name='Students_details'),
    path('developers/Student/notices/', Div_StudentsDetailView.as_view(), name='Students_details'),
    path('developers/Student/classes/', Div_StudentsDetailView.as_view(), name='Students_details'),
    path('developers/Student/library/', Div_StudentsDetailView.as_view(), name='Students_details'),
    path('developers/Student/results/', Div_StudentsDetailView.as_view(), name='Students_details'),
    path('developers/Student/timetables/', Div_StudentsDetailView.as_view(), name='Students_details'),
 
]