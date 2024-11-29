import uuid
from Admin_app.models import *
from datetime import datetime
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, status
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db import DatabaseError, IntegrityError, connection, transaction
from django_countries.fields import CountryField
from django_countries import countries

  

   
class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = '__all__'
        
        
class DevelopersSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    phone_numbers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_address(self, obj):
        try:
            address = Address.objects.get(username=obj.username, entity_type='STAFF')
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
            phone_numbers = PhoneNumbers.objects.filter(username=obj.username, entity_type='STAFF')
            return [pn.phone_number for pn in phone_numbers]
        except PhoneNumbers.DoesNotExist:
            return []


class StaffSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    phone_numbers = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = '__all__'

    def get_address(self, obj):
        try:
            address = Address.objects.get(username=obj.username, entity_type='STAFF')
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
            phone_numbers = PhoneNumbers.objects.filter(username=obj.username, entity_type='STAFF')
            return [pn.phone_number for pn in phone_numbers]
        except PhoneNumbers.DoesNotExist:
            return []

#Applications To The System Serializers

class JobApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplications
        fields = '__all__'

class StudentsEnrolmentSerializer(serializers.ModelSerializer):
    country = serializers.ReadOnlyField(source='get_country_display')

    class Meta:
        model = StudentsEnrolmentsPry
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = {k: v for k, v in data.items() if v and str(v).lower() != 'n/a'}
        return data
        
class AcceptStaffSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    phone_numbers = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ('email', 'address', 'phone_numbers')


    def create(self, validated_data):
        email = validated_data['email']

        if not email:
            raise serializers.ValidationError({"email": "email cannot be empty"})

        try:
            staff_emplyment = JobApplications.objects.get(email=email)
            if Staff.objects.filter(email=email).exists():
                validated_data['enrolled'] = True
            
            username = str(uuid.uuid4())[:30]
            staff, created = Staff.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'name': staff_emplyment.name,
                    'surname': staff_emplyment.surname,
                    'position': staff_emplyment.pPosition,
                    'dob': staff_emplyment.dob,
                    'marital_status': staff_emplyment.Marital_Status,
                    'gender': staff_emplyment.Gender,
                }
            )
                            
            if not created:
                staff.name = staff_emplyment.name
                staff.surname = staff_emplyment.surname
                staff.position = staff_emplyment.pPosition
                staff.dob = staff_emplyment.dob
                staff.marital_status = staff_emplyment.Marital_Status
                staff.gender = staff_emplyment.Gender
                staff.save()
            
            phonenumbers_data = {
                'username': staff.username,
                'entity_type': 'STAFF',
                'phone_number': staff_emplyment.PhoneNumber,
            }
            
            address_data = {
                'username': staff.username,
                'entity_type': 'STAFF',
                'country': staff_emplyment.country,
                'city': staff_emplyment.city,
                'area': staff_emplyment.area,
                'street': staff_emplyment.street,
                'house_number': staff_emplyment.house_number,
            }
            
            Address.objects.update_or_create(username=staff.username, entity_type='STAFF', defaults=address_data)
            PhoneNumbers.objects.update_or_create(username=staff.username, entity_type='STAFF', defaults=phonenumbers_data)

        except JobApplications.DoesNotExist:
            raise serializers.ValidationError({"email": "Staff with this email does not exist."})

        return staff

    def get_phone_numbers(self, obj):
        try:
            phone_numbers = PhoneNumbers.objects.filter(username=obj.username, entity_type='STAFF')
            return [pn.phone_number for pn in phone_numbers]
        except PhoneNumbers.DoesNotExist:
            return []

    def get_address(self, obj):
        try:
            address = Address.objects.get(username=obj.username, entity_type='STAFF')
            return {
                'country': str(address.country), 
                'city': address.city,
                'area': address.area,
                'street': address.street,
                'house_number': address.house_number,
            }
        except Address.DoesNotExist:
            return {}    


class AcceptStudentSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    phone_numbers = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentsPry
        fields = ('email', 'address', 'phone_numbers')

    def create(self, validated_data):
        email = validated_data['email']
        
        if not email:
            raise serializers.ValidationError({"email": "email cannot be empty"})

        try:
            student_enrolment = StudentsEnrolmentsPry.objects.get(email=email)

            year = timezone.now().year
            random_digits = random.randint(1000, 9999)
            random_letter = random.choice(string.ascii_uppercase)
            RegNumber = f"M{year % 100}{random_digits}{random_letter}"
            
            student, created = StudentsPry.objects.get_or_create(
                email=email,
                defaults={
                    'RegNumber': RegNumber,
                    'name': student_enrolment.name,
                    'surname': student_enrolment.surname,
                    'dob': student_enrolment.dob,
                    'gender': student_enrolment.Gender,
                }
            )
            
            if not created:
                student.RegNumber = RegNumber
                student.name = student_enrolment.name
                student.surname = student_enrolment.surname
                student.dob = student_enrolment.dob
                student.gender = student_enrolment.Gender
                student.save()
                
            parent, created = Parents.objects.get_or_create(
                email=student_enrolment.Parent_Email,
                defaults={
                    'username': str(uuid.uuid4())[:30],
                    'name': student_enrolment.Parent_name,
                    'surname': student_enrolment.Parent_surname,
                    'relationship': student_enrolment.Relationship,
                }
            )
            
            if not created:
                parent.name = student_enrolment.Parent_name
                parent.surname = student_enrolment.Parent_surname
                parent.email = student_enrolment.Parent_Email
                parent.relationship = student_enrolment.Relationship
                parent.save()
                
            StudentParent.objects.get_or_create(
                student=student,
                parent=parent,
            )
            
            address_data = {
                'username': student.RegNumber,
                'entity_type': 'STUDENT',
                'country': student_enrolment.country,
                'city': student_enrolment.city,
                'area': student_enrolment.area,
                'street': student_enrolment.street,
                'house_number': student_enrolment.house_number,
            }
            Address.objects.get_or_create(username=student.RegNumber, entity_type='STUDENT', defaults=address_data)
            
            student_phonenumbers_data = {
                'username': student.RegNumber,
                'entity_type': 'STUDENT',
                'phone_number': student_enrolment.Phone_Number,
            }
            PhoneNumbers.objects.get_or_create(username=student.RegNumber, entity_type='STUDENT', defaults=student_phonenumbers_data)
            
            parent_phonenumbers_data = {
                'username': parent.username,
                'entity_type': 'PARENT',
                'phone_number': student_enrolment.Parent_Phone_Number,
            }
            PhoneNumbers.objects.get_or_create(username=parent.username, entity_type='PARENT', defaults=parent_phonenumbers_data)
            
            
            
            classroom = ClassroomsPry.objects.get(grade_level=student_enrolment.Grade_Level)

            class_allocation_pry, created = ClassroomsPry.objects.get_or_create(
                classroom=classroom,
                year=timezone.now().year,
                term=self.determine_term()
            )

            class_allocation_pry.students.add(student)
                            
        except StudentsEnrolmentsPry.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Student with this email does not exist."})

        return student
    
    def get_phone_numbers(self, obj):
        try:
            phone_numbers = PhoneNumbers.objects.filter(username=obj.RegNumber, entity_type='STUDENT')
            return [pn.phone_number for pn in phone_numbers]
        except PhoneNumbers.DoesNotExist:
            return []

    def get_parent_phone_numbers(self, obj):
        try:
            phone_numbers = PhoneNumbers.objects.filter(username=obj.username, entity_type='PARENT')
            return [pn.phone_number for pn in phone_numbers]
        except PhoneNumbers.DoesNotExist:
            return []
        
    def get_address(self, obj):
        try:
            address = Address.objects.get(username=obj.RegNumber, entity_type='STUDENT')
            return {
                'country': str(address.country), 
                'city': address.city,
                'area': address.area,
                'street': address.street,
                'house_number': address.house_number,
            }
        except Address.DoesNotExist:
            return {}    

    def determine_term(self):
        current_month = datetime.now().month
        if current_month in range(1, 4):
            return '1st Term'
        elif current_month in range(4, 8):
            return '2nd Term'
        else:
            return '3rd Term'
    
    
    
#Settings Serilizers

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'password2')
 

#Registrations

class RegisterStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords dodn't match!"})
            
        password = attrs['password']
        if len(password) < 8:
            raise serializers.ValidationError(
                {"password": "Password must be at least 8 characters long."})
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one digit."})
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one letter."})

        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = validated_data['username']
        
        try:
            staff = Staff.objects.get(email=email, name=first_name, surname=last_name)
            PhoneNumbers.objects.filter(username=staff.username).update(username=username)
            Address.objects.filter(username=staff.username).update(username=username)
            Staff.objects.filter(email=email).update(username=username)
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email' : email,
                    'username' : username,
                    'first_name' : staff.name,
                    'last_name' : staff.surname,
                    'role' : staff.position,
                }
            )
          
        except Staff.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Staff with this email, first name and last name does not exist."})

        user.set_password(validated_data['password'])
        user.save()

        return user
   
class RegisterTeacherSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords dodn't match!"})
            
        password = attrs['password']
        if len(password) < 8:
            raise serializers.ValidationError(
                {"password": "Password must be at least 8 characters long."})
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one digit."})
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one letter."})

        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = validated_data['username']
        
        try:
            staff = Staff.objects.get(email=email, name=first_name, surname=last_name)
            PhoneNumbers.objects.filter(username=staff.username).update(username=username)
            Address.objects.filter(username=staff.username).update(username=username)
            Staff.objects.filter(email=email).update(username=username)
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email' : email,
                    'username' : username,
                    'first_name' : staff.name,
                    'last_name' : staff.surname,
                    'role' : 'Teacher'
                }
            )
          
        except Staff.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Staff with this email, first name and last name does not exist."})

        user.set_password(validated_data['password'])
        user.save()

        return user
    
class RegisterStudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords dodn't match!"})
            
        password = attrs['password']
        if len(password) < 8:
            raise serializers.ValidationError(
                {"password": "Password must be at least 8 characters long."})
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one digit."})
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one letter."})

        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        
        try:
            student = StudentsPry.objects.get(RegNumber=username, email=email)
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'username' : student.RegNumber,
                    'first_name' : student.name,
                    'last_name' : student.surname,
                    'email' : student.email,
                    'role' : 'Student'

                }
            )
        except StudentsPry.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Student Doesn't Exist Please Check your details"})

        user.set_password(validated_data['password'])
        user.save()

        return user

class RegisterParentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        email = validated_data['email']
        first_name = self.initial_data.get('first_name')
        last_name = self.initial_data.get('last_name')
        nusername = self.initial_data.get('username')
        country_code = self.initial_data.get('country')
        city = self.initial_data.get('city')
        area = self.initial_data.get('area')
        street = self.initial_data.get('street')
        house_number = self.initial_data.get('house_number')
        phone_number = self.initial_data.get('phone_number')
        id_number = self.initial_data.get('id_number')
        occupation = self.initial_data.get('occupation')

        try:
            with transaction.atomic():
                parent = Parents.objects.get(email=email)
                old_username = parent.username

                Parents.objects.filter(email=email).update(
                    username=nusername,
                    name=first_name,
                    surname=last_name,
                    id_number=id_number,
                    occupation=occupation
                )

                StudentParent.objects.filter(parent_id=old_username).update(parent_id=nusername)

                PhoneNumbers.objects.filter(username=old_username, entity_type='PARENT').update(username=nusername)
                Address.objects.filter(username=old_username, entity_type='PARENT').update(username=nusername)

                PhoneNumbers.objects.get_or_create(
                    username=nusername,
                    entity_type='PARENT',
                    defaults={'phone_number': phone_number}
                )

                Address.objects.update_or_create(
                    username=nusername,
                    entity_type='PARENT',
                    defaults={
                        'country': country_code,
                        'city': city,
                        'area': area,
                        'street': street,
                        'house_number': house_number,
                    }
                )

                user, created = User.objects.update_or_create(
                    username=nusername,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': parent.email,
                        'role': 'Parent/Guardian'
                    }
                )

                user.set_password(validated_data['password'])
                user.save()

        except Parents.DoesNotExist:
            raise ValidationError({'message': 'Parent not found'})
        except DatabaseError as e:
            raise ValidationError({'message': 'Database error: ' + str(e)})
        except Exception as e:
            raise ValidationError({'message': 'An error occurred: ' + str(e)})
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            phone_number = PhoneNumbers.objects.get(username=instance.username, entity_type='PARENT').phone_number
            data['phone_number'] = phone_number
        except PhoneNumbers.DoesNotExist:
            data['phone_number'] = None
        return data  
    
    

#Staff Students and Parents Intro

class StudentListSerializer(serializers.ModelSerializer):
    grade_level = serializers.SerializerMethodField()

    class Meta:
        model = StudentsPry
        fields = ['RegNumber', 'name', 'surname', 'gender', 'grade_level']

    def get_grade_level(self, obj):
        try:
            student_membership = ClassroomsPry.objects.filter(student=obj).latest('id')
            class_allocation = ClassroomsPry.objects.get(id=student_membership.classroom.id)
            grade_level = ClassroomsPry.objects.get(id=class_allocation.classroom.id).grade_level
            return grade_level
        except (ClassroomsPry.DoesNotExist, ClassroomsPry.DoesNotExist, ClassroomsPry.DoesNotExist):
            return None
        
     
class ParentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = ['username', 'name', 'surname']
     
        

#Staff

class TeachersPrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

    def get_queryset(self):
        return Staff.objects.filter(position='Teacher')
        
        

#Students
  
class StudentsSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    phone_numbers = serializers.SerializerMethodField()
    parents = serializers.SerializerMethodField()
    grade_level = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentsPry
        fields = '__all__'
    
    def get_address(self, obj):
        try:
            address = Address.objects.get(username=obj.RegNumber, entity_type='STUDENT')
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
            phone_numbers = PhoneNumbers.objects.filter(username=obj.RegNumber, entity_type='STUDENT')
            return [pn.phone_number for pn in phone_numbers]
        except PhoneNumbers.DoesNotExist:
            return []

    def get_parents(self, obj):
        parents = obj.parent_relationships.all()
        serializer = ParentListSerializer([parent.parent for parent in parents], many=True)
        return serializer.data

    def get_grade_level(self, obj):
        try:
            student_membership = ClassroomsPry.objects.filter(student=obj).latest('id')
            class_allocation = ClassroomsPry.objects.get(id=student_membership.classroom.id)
            grade_level = ClassroomsPry.objects.get(id=class_allocation.classroom.id).grade_level
            return grade_level
        except (ClassroomsPry.DoesNotExist, ClassroomsPry.DoesNotExist, ClassroomsPry.DoesNotExist):
            return None
     
#Parents

class ParentsSerializer(serializers.ModelSerializer):
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
    


#ACCOUNTING
class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = ['total_fees', 'outstanding_balance']



#Academics

class ClassSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()

    class Meta:
        model = ClassroomsPry
        fields = ['grade_level', 'classroom_number', 'teacher']

    def get_teacher(self, obj):
        return f"{obj.teacher.name} {obj.teacher.surname}"

class AssignTeacherSerializer(serializers.Serializer):
    teacher_username = serializers.CharField(max_length=50)
    class_id = serializers.IntegerField()

class CreateClassSerializer(serializers.ModelSerializer):
    teacher = serializers.CharField(write_only=True)

    class Meta:
        model = ClassroomsPry
        fields = ['grade_level', 'classroom_number', 'teacher']

    def create(self, validated_data):
        teacher_username = validated_data.pop('teacher')
        try:
            teacher = Staff.objects.get(username=teacher_username)
            classroom = ClassroomsPry.objects.create(teacher=teacher, **validated_data)
            self.create_class_allocation(classroom)
            return classroom
        except Staff.DoesNotExist:
            raise serializers.ValidationError('Teacher not found')
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def create_class_allocation(self, classroom):
        current_year = datetime.now().year
        term = self.determine_term()
        ClassroomsPry.objects.create(year=current_year, term=term, classroom=classroom)

    def determine_term(self):
        current_month = datetime.now().month
        if current_month in range(1, 4):
            return '1st Term'
        elif current_month in range(4, 8):
            return '2nd Term'
        else:
            return '3rd Term'

      
      
#Teachers
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsPry
        fields = ['RegNumber', 'name', 'surname']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendancePry
        fields = ['student', 'attendance_date', 'status']
    
    
    
    

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
        fields = ['username', 'name', 'surname', 'email', 'children']

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