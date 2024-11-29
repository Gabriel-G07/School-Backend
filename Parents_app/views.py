from pyexpat.errors import messages
from urllib import request
from .forms import *
from .models import *
from Admin_app.models import Parents, ResultsPry
from .serializer import *
from Primary.Students_app.serializer import StudentsSerializer
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

class ParentsDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            parent = Parents.objects.get(username=username)
            serializer = ParentsDetailSerializer(parent)
            return Response(serializer.data)
        except Parents.DoesNotExist:
            return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)

class ParentsFeesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        parent = Parents.objects.get(username=request.user.username)
        serializer = ParentFeesSerializer(parent)
        return Response(serializer.data)
    
     
class ParentsChildDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            parent = Parents.objects.get(username=username)
            children = parent.child_relationships.all()
            serializer = StudentListSerializer([child.student for child in children], many=True)
            return Response(serializer.data)
        except Parents.DoesNotExist:
            return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
class ParentsNoticesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            parent = Parents.objects.get(Username=username)
            serializer = ParentsSerializer(parent)
            return Response(serializer.data)
        except Parents.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        
class ParentsClassesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            parent = Parents.objects.get(Username=username)
            serializer = ParentsSerializer(parent)
            return Response(serializer.data)
        except Parents.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
       
from collections import defaultdict

class ParentsResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        parent = Parents.objects.get(username=username)
        children = StudentsPry.objects.filter(parents=parent)

        results = ResultsPry.objects.filter(student__in=children)
        serializer = ResultsSerializer(results, many=True)

        # Group results by year and term, then by student
        grouped_results = defaultdict(lambda: defaultdict(list))
        for result in serializer.data:
            key = f"{result['year']}-{result['term']}"
            grouped_results[key][result['student_name']].append({
                'subject': result['subject'],
                'grade': result['grade']
            })

        # Convert defaultdict to regular dict
        grouped_results = {key: dict(value) for key, value in grouped_results.items()}

        return Response(grouped_results, status=status.HTTP_200_OK)
    
            
class ParentsTimeTablessView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            parent = Parents.objects.get(Username=username)
            serializer = ParentsSerializer(parent)
            return Response(serializer.data)
        except Parents.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        

class ParentsAttendanceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            parent = Parents.objects.get(username=username)  # Fix: username instead of Username
            serializer = ParentsSerializer(parent)
            return Response(serializer.data)
        except Parents.DoesNotExist:
            return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)  # Fix: Parent instead of Student


class ParentAttendanceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            parent = Parents.objects.get(username=username)
            children = parent.child_relationships.all()
            serializer = ParentAttendanceSerializer([child.student for child in children], many=True)
            return Response(serializer.data)
        except Parents.DoesNotExist:
            return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)