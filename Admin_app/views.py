from pyexpat.errors import messages
from urllib import request
from .forms import *
from .models import *
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



class StudentFeesSerializer(Serializer):
    class Meta:
        fields = ['RegNumber', 'name', 'surname', 'total_amount', 'amount_paid']

    def to_internal_value(self, data):
        return {
            'RegNumber': data.get('reg_number'),
            'name': StudentsPry.objects.get(RegNumber=data.get('reg_number')).name,
            'surname': StudentsPry.objects.get(RegNumber=data.get('reg_number')).surname,
            'total_amount': Fees.objects.filter(student__RegNumber=data.get('reg_number')).first().total_amount if Fees.objects.filter(student__RegNumber=data.get('reg_number')).exists() else 0,
            'amount_paid': Payments.objects.filter(fee__student__RegNumber=data.get('reg_number')).first().amount_paid if Payments.objects.filter(fee__student__RegNumber=data.get('reg_number')).exists() else 0,
        }


class SearchStudentView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentFeesSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            student_data = serializer.to_internal_value(request.data)
            return Response(student_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MakePaymentView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentFeesSerializer

    def create(self, request, *args, **kwargs):
        reg_number = request.data.get('reg_number')
        amount_paid = request.data.get('amount_paid')
        student = StudentsPry.objects.get(RegNumber=reg_number)
        fee, created = Fees.objects.get_or_create(student=student)
        payment, created = Payments.objects.get_or_create(fee=fee)
        payment.amount_paid = amount_paid
        payment.save()
        return Response({'message': 'Payment successful'}, status=status.HTTP_201_CREATED)






@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/token/',
        '/register/',
        '/jobs/applications/',
        ''
    ]
    return Response(routes)


class WebsiteView(View):
    permission_classes = [AllowAny]
 
    def get(self, request, *args, **kwargs):
        if kwargs.get('template') == 'WebsiteHome':
            return render(request, 'website/home.html')
        elif kwargs.get('template') == 'jobs_applications':
            form = JobApplicationsForm()
            return render(request, 'website/admissions/staff_applications.html', {'form': form})
        
        elif kwargs.get('template') == 'students_applications':
            form = StudentEnrolmentForm()
            return render(request, 'website/admissions/student_applications.html', {'form': form})


        elif kwargs.get('template') == 'who-we-are':
            return render(request, 'website/about-us/who-we-are.html')
        elif kwargs.get('template') == 'website_message':
            return render(request, 'website/about-us/message.html')
        elif kwargs.get('template') == 'vision-mission-objectives':
            return render(request, 'website/about-us/objectives/vision-mission-objectives.html')
        elif kwargs.get('template') == 'objectives-detail':
            return render(request, 'website/about-us/objectives/objectives-detail.html')
        elif kwargs.get('template') == 'staff&members':
            return render(request, 'website/about-us/staff&members.html')
        elif kwargs.get('template') == 'resources&facilities':
            return render(request, 'website/about-us/resources&facilities.html')
        elif kwargs.get('template') == 'history':
            return render(request, 'website/about-us/history.html')
        elif kwargs.get('template') == 'academic-information':
            return render(request, 'website/academics/academic-information.html')
        elif kwargs.get('template') == 'academic_grades':
            return render(request, 'website/academics/academic-grades.html')
        elif kwargs.get('template') == 'admission-notices':
            return render(request, 'website/admissions/admission-notices.html')
        elif kwargs.get('template') == 'news':
            return render(request, 'website/news/news.html')
        elif kwargs.get('template') == 'event':
            return render(request, 'website/events/event.html')
        elif kwargs.get('template') == 'event-details':
            return render(request, 'website/events/event-details.html')
        elif kwargs.get('template') == 'our-blog':
            return render(request, 'website/blog/our-blog.html')
        elif kwargs.get('template') == 'blog-details':
            return render(request, 'website/blog/blog-details.html')
        elif kwargs.get('template') == 'contact':
            return render(request, 'website/contact/contact.html')
        elif kwargs.get('template') == 'our-team':
            return render(request, 'website/team.html')
        elif kwargs.get('template') == 'service-details':
            return render(request, 'website/about-us/service.html')
        elif kwargs.get('template') == 'gallery':
            return render(request, 'website/resources/gallery.html')
        else:
            return render(request, 'website/resources/error.html', status=404)

    def post(self, request, *args, **kwargs):
        if kwargs.get('template') == 'jobs_applications':
            form = JobApplicationsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('WebsiteHome')
        elif kwargs.get('template') == 'students_applications':
            form = StudentEnrolmentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admission-notices')
        return render(request, 'website/home.html', {'form': form})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
class RegisterStaffView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterStaffSerializer
 
 
class RegisterTeacherView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterTeacherSerializer
    
    
class RegisterStudentView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterStudentSerializer
        
class RegisterParentSearchStudentView(APIView):
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
   
    
class RegisterParentView(generics.CreateAPIView):
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
    
    
class UserSettingsView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = SettingsSerializer
    
class StaffDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.username
        try:
            staff = Staff.objects.get(username=username)
            serializer = StaffSerializer(staff)
            return Response(serializer.data)
        except Staff.DoesNotExist:
            return Response({"error": "Staff not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
class StaffView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        staff = Staff.objects.all()
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data)
    
        
class TeachersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        teachers = Staff.objects.filter(position='Teacher')
        serializer = TeachersPrySerializer(teachers, many=True)
        return Response(serializer.data)
    
class ClassesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        staff = ClassroomsPry.objects.all()
        serializer = ClassSerializer(staff, many=True)
        return Response(serializer.data)
    
class StudentsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        students = StudentsPry.objects.all()
        serializer = StudentsSerializer(students, many=True)
        return Response(serializer.data)
    
class ParentsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        parents = Parents.objects.all()
        serializer = ParentsSerializer(parents, many=True)
        return Response(serializer.data)
    
class JobApplicationsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        staff = JobApplications.objects.all()
        serializer = JobApplicationsSerializer(staff, many=True)
        return Response(serializer.data)
    
class StudentsEnrolmentView(APIView):
    def get(self, request):
        students = StudentsEnrolmentsPry.objects.all()
        serializer = StudentsEnrolmentSerializer(students, many=True)
        return Response(serializer.data)
    
class CreateClassView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CreateClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Class created, teacher assigned, and class allocation set'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
   
   
class SearchStudentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        reg_number = request.data['reg_number']
        try:
            student = StudentsPry.objects.get(RegNumber=reg_number)
            serializer = StudentsSerializer(student)
            return Response(serializer.data)
        except StudentsPry.DoesNotExist:
            return Response({})

class MakePaymentView(APIView):
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
   
   
   
   
   
   
   
   
   
   
   
   
   
    
class AcceptedJobApplicationsView(generics.CreateAPIView):
    queryset = Staff.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AcceptStaffSerializer
    
class AcceptedStudentsEnrolmentView(generics.CreateAPIView):
    queryset = StudentsPry.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AcceptStudentSerializer