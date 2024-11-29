from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('parent/details/', ParentsDetailView.as_view(), name='Parents_details'),
    path('parent/child/details/', ParentsChildDetailsView.as_view(), name='Parents_child_details'),
    path('parent/notices/', ParentsNoticesView.as_view(), name='Parents_noticess'),
    path('parent/classes/', ParentsClassesView.as_view(), name='Parents_classes'),
    path('parent/fees/', ParentsFeesView.as_view(), name='Parents_fees'),
    path('parent/results/', ParentsResultsView.as_view(), name='Parents_results'),
    path('parent/timetables/', ParentsTimeTablessView.as_view(), name='Parents_timetables'),
    path('parent/attendance/', ParentsAttendanceView.as_view()),
]