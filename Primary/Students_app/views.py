from pyexpat.errors import messages
from urllib import request
from .forms import *
from .models import *
from Admin_app.models import StudentsPry
from .serializer import *
from django.views import View
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.forms import inlineformset_factory, modelformset_factory
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.password_validation import validate_password
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie



class StudentsDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            student = StudentsPry.objects.get(RegNumber=username)
            serializer = StudentsSerializer(student)
            return Response(serializer.data)
        except StudentsPry.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        

        

