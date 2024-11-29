from pyexpat.errors import messages
from urllib import request
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
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.serializers import Serializer
from collections import defaultdict

    
class Div_SaveCampusView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CampusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Campus Saved Successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Div_CampusesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        campus = Campus.objects.all()
        serializer = CampusSerializer(campus, many=True)
        return Response(serializer.data)
        
   


class Div_StudentFeesSerializer(Serializer):
    class Div_Meta:
        fields = ['RegNumber', 'name', 'surname', 'total_amount', 'amount_paid']

    def to_internal_value(self, data):
        return {
            'RegNumber': data.get('reg_number'),
            'name': StudentsPry.objects.get(RegNumber=data.get('reg_number')).name,
            'surname': StudentsPry.objects.get(RegNumber=data.get('reg_number')).surname,
            'total_amount': Fees.objects.filter(student__RegNumber=data.get('reg_number')).first().total_amount if Fees.objects.filter(student__RegNumber=data.get('reg_number')).exists() else 0,
            'amount_paid': Payments.objects.filter(fee__student__RegNumber=data.get('reg_number')).first().amount_paid if Payments.objects.filter(fee__student__RegNumber=data.get('reg_number')).exists() else 0,
        }


class Div_SearchStudentView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeesSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            student_data = serializer.to_internal_value(request.data)
            return Response(student_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Div_MakePaymentView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeesSerializer

    def create(self, request, *args, **kwargs):
        reg_number = request.data.get('reg_number')
        amount_paid = request.data.get('amount_paid')
        student = StudentsPry.objects.get(RegNumber=reg_number)
        fee, created = Fees.objects.get_or_create(student=student)
        payment, created = Payments.objects.get_or_create(fee=fee)
        payment.amount_paid = amount_paid
        payment.save()
        return Response({'message': 'Payment successful'}, status=status.HTTP_201_CREATED)



class Div_RegisterStaffView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterStaffSerializer
 
 
class Div_RegisterTeacherView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterTeacherSerializer
    
    
class Div_RegisterStudentView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterStudentSerializer
        
class Div_RegisterParentSearchStudentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_numbers = request.data.get('regNumbers', [])
        students = StudentsPry.objects.filter(RegNumber__in=reg_numbers)

        found_students = students.values('name', 'surname')
        not_found_reg_numbers = [reg for reg in reg_numbers if reg not in students.values_list('RegNumber', flat=True)]

        if found_students.count() == 1:
            return Response({'message': f'Is your student {found_students[0]["name"]} {found_students[0]["surname"]}?'})
        elif found_students.count() > 1:
            student_names = ', '.join([f'{student["name"]} {student["surname"]}' for student in found_students])
            return Response({'message': f'Are your children {student_names}?'})
        else:
            if len(not_found_reg_numbers) == 1:
                return Response({'message': f'We have no student with the following RegNumber {not_found_reg_numbers[0]}', 'error': True}, status=404)
            else:
                return Response({'message': f'Students with these RegNumbers {", ".join(not_found_reg_numbers)} were not found', 'error': True}, status=404)
   
    
class Div_RegisterParentView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterParentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': 'Parent registered successfully'}, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class Div_UserSettingsView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = SettingsSerializer
    
class Div_DetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            staff = User.objects.get(username=username)
            serializer = DevelopersSerializer(staff)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
class Div_StaffView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        staff = Staff.objects.all()
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data)
    
        
class Div_TeachersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        teachers = Staff.objects.filter(position='Teacher')
        serializer = TeachersPrySerializer(teachers, many=True)
        return Response(serializer.data)
    
class Div_ClassesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        staff = ClassroomsPry.objects.all()
        serializer = ClassSerializer(staff, many=True)
        return Response(serializer.data)
    
class Div_StudentsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        students = StudentsPry.objects.all()
        serializer = StudentsSerializer(students, many=True)
        return Response(serializer.data)
    
class Div_ParentsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        parents = Parents.objects.all()
        serializer = ParentsSerializer(parents, many=True)
        return Response(serializer.data)
    
class Div_JobApplicationsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        staff = JobApplications.objects.all()
        serializer = JobApplicationsSerializer(staff, many=True)
        return Response(serializer.data)
    
class Div_StudentsEnrolmentView(APIView):
    def get(self, request):
        students = StudentsEnrolmentsPry.objects.all()
        serializer = StudentsEnrolmentSerializer(students, many=True)
        return Response(serializer.data)
    
class Div_CreateClassView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CreateClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Class created, teacher assigned, and class Div_allocation set'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
   
   
class Div_SearchStudentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        reg_number = request.data['reg_number']
        try:
            student = StudentsPry.objects.get(RegNumber=reg_number)
            serializer = StudentsSerializer(student)
            return Response(serializer.data)
        except StudentsPry.DoesNotExist:
            return Response({})

class Div_MakePaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        reg_number = request.data['reg_number']
        amount_paid = request.data['amount_paid']
        try:
            student = StudentsPry.objects.get(RegNumber=reg_number)
            fee = Fees.objects.get(student=student)
            payment = Payments(
                student=student,
                fee=fee,
                amount=amount_paid
            )
            payment.save()
            return Response({'message': 'Payment successful'})
        except (StudentsPry.DoesNotExist, Fees.DoesNotExist):
            return Response({'error': 'Student or fee not found'})
   
   
   
   
   
   
    
class Div_AcceptedJobApplicationsView(generics.CreateAPIView):
    queryset = Staff.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AcceptStaffSerializer


class Div_AcceptedStudentsEnrolmentView(generics.CreateAPIView):
    queryset = StudentsPry.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AcceptStudentSerializer
    
    

class Div_ParentsDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            parent = Parents.objects.get(username=username)
            serializer = ParentsDetailSerializer(parent)
            return Response(serializer.data)
        except Parents.DoesNotExist:
            return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)

class Div_ParentsFeesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        parent = Parents.objects.get(username=request.user.username)
        serializer = ParentFeesSerializer(parent)
        return Response(serializer.data)
    
     
class Div_ParentsChildDetailsView(APIView):
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
        
        
class Div_ParentsNoticesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            parent = Parents.objects.get(Username=username)
            serializer = ParentsSerializer(parent)
            return Response(serializer.data)
        except Parents.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        
class Div_ParentsClassesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            parent = Parents.objects.get(Username=username)
            serializer = ParentsSerializer(parent)
            return Response(serializer.data)
        except Parents.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

class Div_ParentsResultsView(APIView):
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
    
            
class Div_ParentsTimeTablessView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            parent = Parents.objects.get(Username=username)
            serializer = ParentsSerializer(parent)
            return Response(serializer.data)
        except Parents.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        

class Div_ParentsAttendanceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            parent = Parents.objects.get(username=username)  # Fix: username instead of Username
            serializer = ParentsSerializer(parent)
            return Response(serializer.data)
        except Parents.DoesNotExist:
            return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)  # Fix: Parent instead of Student


class Div_ParentAttendanceView(APIView):
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
        
        
        
        
#Students
class Div_StudentsDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            student = StudentsPry.objects.get(RegNumber=username)
            serializer = StudentsSerializer(student)
            return Response(serializer.data)
        except StudentsPry.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        

#Teachers
class Div_TeacherStudentsView(APIView):
    def get(self, request):
        teacher = request.user.username
        classroom = ClassroomsPry.objects.get(teacher=teacher)
        classroom_allocation = ClassroomsPry.objects.get(classroom=classroom)
        students = classroom_allocation.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    

class Div_MarkAttendanceView(APIView):
    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

