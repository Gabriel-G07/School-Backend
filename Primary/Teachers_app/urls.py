from django.urls import path
from . import views
from .views import *
from Admin_app.views import *
from django.urls import re_path

urlpatterns = [

    path('classes/primary/students/', TeacherStudentsView.as_view()),
    path('attendance/mark/', MarkAttendanceView.as_view()),
 
]