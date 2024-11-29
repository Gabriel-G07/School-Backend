from django.urls import path
from . import views
from .views import *
from django.urls import re_path

urlpatterns = [
    path('routes/', views.getRoutes),
    
    #Web Site Urls
    path('', WebsiteView.as_view(), name='WebsiteHome', kwargs={'template': 'WebsiteHome'}),
    path('home/', WebsiteView.as_view(), name='WebsiteHome', kwargs={'template': 'WebsiteHome'}),
    path('jobs/applications/', WebsiteView.as_view(), name='jobs_applications', kwargs={'template': 'jobs_applications'}),
    path('student/application/', WebsiteView.as_view(), name='students_applications', kwargs={'template': 'students_applications'}),
    path('aboutus/', WebsiteView.as_view(), name='who-we-are', kwargs={'template': 'who-we-are'}),
    path('message/', WebsiteView.as_view(), name='website_message', kwargs={'template': 'website_message'}),
    path('visions/missions/objectives/', WebsiteView.as_view(), name='vision-mission-objectives', kwargs={'template': 'vision-mission-objectives'}),
    path('team/staff/', WebsiteView.as_view(), name='staff&members', kwargs={'template': 'staff&members'}),
    path('academics/resources/', WebsiteView.as_view(), name='resources&facilities', kwargs={'template': 'resources&facilities'}),
    path('history/', WebsiteView.as_view(), name='history', kwargs={'template': 'history'}),
    path('academics/information/', WebsiteView.as_view(), name='academic-information', kwargs={'template': 'academic-information'}),
    path('academics/grades/', WebsiteView.as_view(), name='academic_grades', kwargs={'template': 'academic_grades'}),
    path('admissions/notes/', WebsiteView.as_view(), name='admission-notices', kwargs={'template': 'admission-notices'}),
    path('news/', WebsiteView.as_view(), name='news', kwargs={'template': 'news'}),
    path('events/', WebsiteView.as_view(), name='event', kwargs={'template': 'event'}),
    path('events/details/', WebsiteView.as_view(), name='event-details', kwargs={'template': 'event-details'}),
    path('blog/', WebsiteView.as_view(), name='our-blog', kwargs={'template': 'our-blog'}),
    path('blog/details/', WebsiteView.as_view(), name='blog-details', kwargs={'template': 'blog-details'}),
    path('contact-details/', WebsiteView.as_view(), name='contact', kwargs={'template': 'contact'}),
    path('team/', WebsiteView.as_view(), name='our-team', kwargs={'template': 'our-team'}),
    path('objectives/details/', WebsiteView.as_view(), name='objectives-detail', kwargs={'template': 'objectives-detail'}),
    path('services/details/', WebsiteView.as_view(), name='service-details', kwargs={'template': 'service-details'}),
    path('gallery/', WebsiteView.as_view(), name='gallery', kwargs={'template': 'gallery'}),
    
    
 
    
    #Signup urls
    path('admin_token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('student_token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('parent_token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('developers_token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/developer/', RegisterTeacherView.as_view(), name='auth_register_teacher'),
    path('register/staff/', RegisterStaffView.as_view(), name='auth_register_staff'),
    path('register/student/', RegisterStudentView.as_view(), name='auth_register_student'),
    path('register/teacher/', RegisterTeacherView.as_view(), name='auth_register_teacher'),
    path('parent/register/search/students/', RegisterParentSearchStudentView.as_view(), name='auth_register_parent_search_student'),
    path('register/parent/', RegisterParentView.as_view(), name='auth_register_parent'),
    
    
    #Main Admin
    path('staff/details/', StaffDetailView.as_view(), name='staff_details'),
    path('staff/', StaffView.as_view(), name='staff'),
    path('students/', StudentsView.as_view(), name='students'),
    path('parents/', ParentsView.as_view(), name='parents'),
    path('staff/job/applications/', JobApplicationsView.as_view(), name='staff_job_applications'),
    path('students/enrolments/', StudentsEnrolmentView.as_view(), name='students_enrolments'),
    path('staff/job/applications/accepted/', AcceptedJobApplicationsView.as_view(), name='staff_job_applications_accepted'),
    path('students/enrolments/accepted/', AcceptedStudentsEnrolmentView.as_view(), name='students_enrolments_accepted'),
    path('admin/fees/search/', SearchStudentView.as_view()),
    path('admin/fees/payment/', MakePaymentView.as_view()),
    path('create-class/', CreateClassView.as_view(), name='create-class'),
    path('teachers/', TeachersView.as_view()),
    path('classes/', ClassesView.as_view()),
]