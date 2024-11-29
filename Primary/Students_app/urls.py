from django.urls import path
from . import views
from .views import *
from django.urls import re_path

urlpatterns = [

    #Students
    path('Student/dashboard/', StudentsDetailView.as_view(), name='Students_details'),
    path('Student/details/', StudentsDetailView.as_view(), name='Students_details'),
    path('Student/notices/', StudentsDetailView.as_view(), name='Students_details'),
    path('Student/classes/', StudentsDetailView.as_view(), name='Students_details'),
    path('Student/library/', StudentsDetailView.as_view(), name='Students_details'),
    path('Student/results/', StudentsDetailView.as_view(), name='Students_details'),
    path('Student/timetables/', StudentsDetailView.as_view(), name='Students_details'),
 
]