from django.urls import include, path

urlpatterns = [
    path('', include('Primary.Students_app.urls')),
    path('', include('Primary.Teachers_app.urls')),
]