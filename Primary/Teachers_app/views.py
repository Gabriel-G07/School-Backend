from django.shortcuts import render
from Admin_app.models import *
from Admin_app.serializer import StudentSerializer, AttendanceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class TeacherStudentsView(APIView):
    def get(self, request):
        teacher = request.user.username
        classroom = ClassroomsPry.objects.get(teacher=teacher)
        classroom_allocation = ClassroomsPry.objects.get(classroom=classroom)
        students = classroom_allocation.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    

class MarkAttendanceView(APIView):
    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)