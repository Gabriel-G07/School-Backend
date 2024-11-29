import uuid
from .models import *
from Admin_app.models import Parents, ClassroomsPry, StudentsPry, Address, PhoneNumbers, StudentAttendancePry, Fees, ResultsPry
from Admin_app.serializer import StudentListSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.db.models.signals import post_save
from django.dispatch import receiver

class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = '__all__'
        
class ParentsDetailSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    phone_numbers = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Parents
        fields = '__all__'
        
    
    def get_address(self, obj):
        try:
            address = Address.objects.get(username=obj.username, entity_type='PARENT')
            data = {
                'country': address.get_country_display(),
                'city': address.city,
                'area': address.area,
                'street': address.street,
                'house_number': address.house_number,
            }
            
            data = {k: v for k, v in data.items() if v and str(v).lower() != 'n/a'}
            
            if len(data) > 1:
                return data
            else:
                return {}
        except Address.DoesNotExist:
            return {}

    def get_phone_numbers(self, obj):
        try:
            phone_numbers = PhoneNumbers.objects.filter(username=obj.username, entity_type='PARENT')
            return [pn.phone_number for pn in phone_numbers]
        except PhoneNumbers.DoesNotExist:
            return []
        

    def get_children(self, obj):
        children = obj.child_relationships.all()
        serializer = StudentListSerializer([child.student for child in children], many=True)
        return serializer.data

class ParentChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsPry
        fields = ['RegNumber', 'name', 'surname', 'email', 'image']

class ParentFeesSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Parents
        fields = ['username', 'name', 'surname', 'children']

    def get_children(self, obj):
        children = StudentsPry.objects.filter(parents=obj)
        serializer = ChildFeesSerializer(children, many=True)
        return serializer.data

class ChildFeesSerializer(serializers.ModelSerializer):
    fees = serializers.SerializerMethodField()
    grade_level = serializers.SerializerMethodField()

    class Meta:
        model = StudentsPry
        fields = ['RegNumber', 'name', 'surname', 'grade_level', 'fees']

    def get_fees(self, obj):
        fees = Fees.objects.filter(student=obj)
        serializer = FeesSerializer(fees, many=True)
        return serializer.data

    def get_grade_level(self, obj):
        class_membership = ClassroomsPry.objects.filter(student=obj).first()
        if class_membership:
            return class_membership.classroom.classroom.grade_level
        return None

class FeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = ['year', 'term', 'new_term_fees', 'total_fees', 'fees_paid', 'outstanding_balance']

class ParentChildDetailsSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Parents
        fields = ['Username', 'Name', 'Surname', 'Email', 'children']

    def get_children(self, obj):
        parent_username = self.context['request'].user.username
        children = StudentsPry.objects.filter(Parent__Username=parent_username)
        return ParentChildSerializer(children, many=True).data

class ResultsSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = ResultsPry
        fields = ['student_name', 'subject', 'grade', 'term', 'year']

    def get_student_name(self, obj):
        return f"{obj.student.name} {obj.student.surname}"

class ParentAttendanceSerializer(serializers.ModelSerializer):
    attendance = serializers.SerializerMethodField()

    class Meta:
        model = StudentsPry
        fields = ['RegNumber', 'name', 'surname', 'attendance']

    def get_attendance(self, obj):
        attendance = StudentAttendancePry.objects.filter(student=obj)
        serializer = StudentAttendancePrySerializer(attendance, many=True)
        return serializer.data
    
class StudentAttendancePrySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendancePry
        fields = ['attendance_date', 'status']