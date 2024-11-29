import datetime, random, string
from datetime import datetime, timezone
from django.utils import timezone
from django.db import connection, models
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.signals import pre_save, post_save
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

#Applications To The Sytem

class JobApplications(models.Model):
    class Meta:
        db_table = 'JobApplications'

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    Gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    PhoneNumber = models.CharField(max_length=20)
    pPosition = models.CharField(max_length=50)
    dob = models.DateField(verbose_name="Date of Birth")
    Marital_Status = models.CharField(max_length=20, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divoced', 'Divoced')])
    email = models.EmailField()
    country = CountryField()
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house_number = models.CharField(max_length=20)

class StudentsEnrolmentsPry(models.Model):
    class Meta:
        db_table = 'EnrolmentApplications'
        
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    Gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    dob = models.DateField()
    email = models.EmailField(unique=True)
    Phone_Number = models.CharField(max_length=20)
    Grade_Level = models.CharField(max_length=20, choices=[
        ('ECD A', 'ECD A'),
        ('ECD B', 'ECD B'),
        ('Grade 1', 'Grade 1'),
        ('Grade 2', 'Grade 2'),
        ('Grade 3', 'Grade 3'),
        ('Grade 4', 'Grade 4'),
        ('Grade 5', 'Grade 5'),
        ('Grade 6', 'Grade 6'),
        ('Grade 7', 'Grade 7'),
    ])
    country = CountryField()
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house_number = models.CharField(max_length=20)
    
    # Parent information
    Parent_name = models.CharField(max_length=100)
    Parent_surname = models.CharField(max_length=100)
    Parent_Email = models.EmailField()
    Relationship = models.CharField(max_length=20)
    Parent_Phone_Number = models.CharField(max_length=20)
    



#Authentication

class CustomUserManager(UserManager):
    def create_user(self, username, first_name, last_name, email, password, role):
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            first_name=first_name, 
            last_name=last_name,
            email=email,
            role=role
        )
        user.set_password(password)
        user.last_login = timezone.now()
        user.save(using=self._db)
        return user

class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'
        auto_created = False
    
    username = models.CharField(max_length=150, primary_key=True, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(max_length=50)
    is_online = models.BooleanField(default=False)
    last_logout = models.DateTimeField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    settings = models.TextField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE, related_name='user_campus', null=True)
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role', 'email']
    
    def __str__(self):
        return self.username
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.role in ['Teacher', 'Head', 'Vice Head', 'Director', 'Developer']:
            self.is_staff = True
        else:
            self.is_staff = False

        self.last_login = datetime.now()

        super().save(*args, **kwargs)

class Campus(models.Model):
    class Meta:
        db_table = 'Campus'

    name = models.CharField(max_length=50, db_index=True)
    schooltype = models.CharField(max_length=13, choices=[('Primary', 'Primary'), ('High School', 'High School')])
    location = models.CharField(max_length=50, db_index=True)
    

#Staff
class Developer(models.Model):
    class Meta:
        db_table = 'Developers'
        
    username = models.CharField(max_length=50, primary_key=True, db_index=True)
    name = models.CharField(max_length=50, db_index=True)
    surname = models.CharField(max_length=50, db_index=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    position = models.CharField(max_length=50)
    dob = models.DateField()
    marital_status = models.CharField(max_length=20, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')])
    email = models.EmailField(unique=True, db_index=True)
    profile_photo = models.ImageField(upload_to="developer_images/", default="default.jpg", blank=True, null=True)
    address = models.OneToOneField('Address', on_delete=models.CASCADE, related_name='developer_address', null=True, blank=True)
    phone_numbers = models.ManyToManyField('PhoneNumbers', related_name='developer_phone_numbers')
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE, related_name='developer_campus')
    
class Staff(models.Model):
    class Meta:
        db_table = 'Staff'

    username = models.CharField(max_length=50, primary_key=True, db_index=True)
    name = models.CharField(max_length=50, db_index=True)
    surname = models.CharField(max_length=50, db_index=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    position = models.CharField(max_length=50)
    dob = models.DateField()
    marital_status = models.CharField(max_length=20, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')])
    email = models.EmailField(unique=True, db_index=True)
    profile_photo = models.ImageField(upload_to="staff_images/", default="default.jpg", blank=True, null=True)
    address = models.OneToOneField('Address', on_delete=models.CASCADE, related_name='staff_address', null=True, blank=True)
    phone_numbers = models.ManyToManyField('PhoneNumbers', related_name='staff_phone_numbers')
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE, related_name='staff_campus')

#Students

class StudentsPry(models.Model):
    class Meta:
        db_table = 'StudentsPry'

    RegNumber = models.CharField(max_length=8, primary_key=True, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=50, db_index=True)
    surname = models.CharField(max_length=50, db_index=True)
    gender = models.CharField(max_length=6)
    dob = models.DateField()
    email = models.EmailField(unique=True, db_index=True)
    class_allocation = models.ForeignKey('ClassroomsPry', on_delete=models.CASCADE, related_name='class_allocations')
    parents = models.ManyToManyField('Parents', through='StudentParent')
    address = models.OneToOneField('Address', on_delete=models.CASCADE, related_name='student_address', null=True, blank=True)
    phone_numbers = models.ManyToManyField('PhoneNumbers', related_name='student_phone_numbers')
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE, related_name='student_campus')
    profile_photo = models.ImageField(upload_to="student_images/", default="default.jpg", blank=True, null=True)

    

class StudentAttendancePry(models.Model):
    class Meta:
        db_table = 'StudentsAttendancePry'
        unique_together = ['student', 'attendance_date']

    student = models.ForeignKey('StudentsPry', on_delete=models.CASCADE, db_index=True)
    term = models.ForeignKey('AcademicCalender', on_delete=models.CASCADE, db_index=True)
    attendance_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    
       
    

#Students arens Relationship

class StudentParent(models.Model):
    class Meta:
        db_table = 'Link_StudentParent'

    student = models.ForeignKey('StudentsPry', on_delete=models.CASCADE, related_name='parent_relationships', db_index=True)
    parent = models.ForeignKey('Parents', on_delete=models.CASCADE, related_name='child_relationships', db_index=True)
    unique_together = ['student', 'parent']



#Parents

class Parents(models.Model):
    class Meta:
        db_table = 'Parents'

    username = models.CharField(max_length=50, primary_key=True, db_index=True)
    name = models.CharField(max_length=50, db_index=True)
    surname = models.CharField(max_length=50, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    id_number = models.CharField(max_length=20, unique=True, db_index=True)
    occupation = models.CharField(max_length=50)
    relationship = models.CharField(max_length=20)
    address = models.OneToOneField('Address', on_delete=models.CASCADE, related_name='parent_address', null=True, blank=True)
    phone_numbers = models.ManyToManyField('PhoneNumbers', related_name='parent_phone_numbers')
    
    profile_photo = models.ImageField(upload_to="parents_images/", default="default.jpg", blank=True, null=True)


#Contact Details For All

class Address(models.Model):
    class Meta:
        db_table = 'Addresses'

    ENTITY_TYPES = [
        ('DEVELOPER', 'Developer'),
        ('STAFF', 'Staff'),
        ('PARENT', 'Parent'),
        ('STUDENT', 'Student')
    ]

    username = models.CharField(max_length=50, db_index=True)
    entity_type = models.CharField(max_length=10, choices=ENTITY_TYPES)
    country = CountryField()
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house_number = models.CharField(max_length=20)
    unique_together = ['username', 'entity_type']

class PhoneNumbers(models.Model):
    class Meta:
        db_table = 'Phone_Numbers'

    ENTITY_TYPES = [
        ('DEVELOPER', 'Developer'),
        ('STAFF', 'Staff'),
        ('PARENT', 'Parent'),
        ('STUDENT', 'Student')
    ]

    username = models.CharField(max_length=50, db_index=True)
    entity_type = models.CharField(max_length=10, choices=ENTITY_TYPES)
    phone_number = models.CharField(max_length=20, unique=True)
    unique_together = ['username', 'entity_type', 'phone_number']

  
    
    
#Academics

class AcademicCalender (models.Model):
    class Meta:
        db_table = 'Calender'

    year = models.IntegerField(validators=[MinValueValidator(2013), MaxValueValidator(2100)], db_index=True)
    term = models.CharField(max_length=20, choices=[
        ('First', 'First'),
        ('Second', 'Second'),
        ('Third', 'Third'),
        ('Holyday April', 'Holyday April'),
        ('Holyday August', 'Holyday August'),
        ('Holyday December', 'Holyday December')
    ])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    term_fees = models.DecimalField(max_digits=5, decimal_places=2)


class ClassroomsPry(models.Model):
    class Meta:
        db_table = 'Classrooms'
        
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE, related_name='classrooms_campus')
    room_number = models.CharField(max_length=10)
    class_teacher = models.ForeignKey('Staff', null=True, on_delete=models.CASCADE, db_index=True, limit_choices_to={'position': 'TeacherPry'})
    class_level = models.CharField(max_length=10, choices=[
        ('ECD A', 'ECD A'),
        ('ECD B', 'ECD B'),
        ('Grade 1', 'Grade 1'),
        ('Grade 2', 'Grade 2'),
        ('Grade 3', 'Grade 3'),
        ('Grade 4', 'Grade 4'),
        ('Grade 5', 'Grade 5'),
        ('Grade 6', 'Grade 6'),
        ('Grade 7', 'Grade 7'),
    ])
    class_code = models.CharField(max_length=20, choices=[
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Green', 'Green'),
        ('Yellow', 'Yellow'),
    ])
    

class SubjectsPry(models.Model):
    class Meta:
        db_table = 'SubjectsPry'

    subject_name = models.CharField(max_length=50)
    paper_number = models.CharField(max_length=10, choices=[('1', '1'), ('2', '2')])
    



#Results And Other Marks

class ClassWorkPry(models.Model):
    class Meta:
        db_table = 'ClassWorkPry'
        
    student = models.ForeignKey('StudentsPry', on_delete=models.CASCADE, db_index=True)
    term = models.ForeignKey('AcademicCalender', on_delete=models.CASCADE, db_index=True)
    subject =  models.ForeignKey('SubjectsPry', on_delete=models.CASCADE, db_index=True)
    date = models.DateTimeField()
    mark = models.IntegerField()
    total_mark = models.IntegerField()
    
    
class ExamMarksPry(models.Model):
    class Meta:
        db_table = 'ExamMarksPry'
        
    student = models.ForeignKey('StudentsPry', on_delete=models.CASCADE, db_index=True)
    term = models.ForeignKey('AcademicCalender', on_delete=models.CASCADE, db_index=True)
    subject =  models.ForeignKey('SubjectsPry', on_delete=models.CASCADE, db_index=True)
    date = models.DateTimeField()
    mark = models.IntegerField()
    total_marks = models.IntegerField(null=False)
    total_mark = models.IntegerField()


class ResultsPry(models.Model):
    class Meta:
        db_table = 'ResultsPry'

    student = models.ForeignKey('StudentsPry', on_delete=models.CASCADE, db_index=True)
    subject = models.ForeignKey('SubjectsPry', on_delete=models.CASCADE, db_index=True)
    term = models.ForeignKey('AcademicCalender', on_delete=models.CASCADE, db_index=True)
    course_work = models.IntegerField(null=False)
    p1_exam_mark = models.IntegerField()
    p2_exam_mark = models.IntegerField()
    exams_total_mark = models.CharField(max_length=3)
    total = models.IntegerField()
    symble = models.IntegerField()
    unique_together = ['student', 'subject', 'term', 'year']

    SYMBOL_RANGES = {
        range(75, 101): 1,
        range(70, 75): 2,
        range(65, 70): 3,
        range(60, 65): 4,
        range(55, 60): 5,
        range(50, 55): 6,
        range(45, 50): 7,
        range(40, 45): 8,
        range(0, 40): 9
    }

    @property
    def coursework_percentage(self):
        coursework_entries = ClassWorkPry.objects.filter(
            student=self.student,
            subject=self.subject,
            term=self.term
        )
        total_marks = 0
        total_score = 0
        for entry in coursework_entries:
            total_marks += entry.total_mark
            total_score += entry.mark
        
        if total_marks > 0:
            return round((total_score / total_marks) * 100, 2)
        return 0.0
    
    @property
    def p1_exam_mark_percentage(self):
        p1_mark = ExamMarksPry.objects.filter(
            student=self.student,
            term=self.term,
            subject=self.subject,
            paper_type=1
        ).last()
        if p1_mark:
            return round((p1_mark.mark / p1_mark.total_mark) * 100, 2)
        return 0.0
    
    @property
    def p2_exam_mark_percentage(self):
        p2_mark = ExamMarksPry.objects.filter(
            student=self.student,
            term=self.term,
            subject=self.subject,
            paper_type=2
        ).last()
        if p2_mark:
            return round((p2_mark.mark / p2_mark.total_mark) * 100, 2)
        return 0.0
    
    def calculate_symbol(self):
        for r, symbol in self.SYMBOL_RANGES.items():
            if self.total in r:
                return symbol
    
    def save(self, *args, **kwargs):
        self.course_work = self.coursework_percentage
        self.p1_exam_mark = self.p1_exam_mark_percentage
        self.p2_exam_mark = self.p2_exam_mark_percentage
        self.exams_total_mark = f"{self.p1_exam_mark}% + {self.p2_exam_mark}%"
        #Making each paper weigh 33%
        self.total = round((self.course_work + self.p1_exam_mark + self.p2_exam_mark) / 3)
        
        self.symble = self.calculate_symbol()
        super().save(*args, **kwargs) 




#Finance and Accounting
class Fees(models.Model):
    class Meta:
        db_table = 'Fees'

    student = models.ForeignKey('StudentsPry', on_delete=models.CASCADE, related_name='fees', db_index=True)
    term = models.ForeignKey('AcademicCalender', limit_choices_to={'term__in': ['First', 'Second', 'Third']}, on_delete=models.CASCADE, related_name='term_details', db_index=True)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    fees_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    outstanding_balance = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        previous_term_fees = Fees.objects.filter(student=self.student, term__id__lt=self.term.id).last()
        if previous_term_fees:
            self.opening_balance = previous_term_fees.outstanding_balance
        self.total_fees = self.opening_balance + self.term.fees
        self.outstanding_balance = self.total_fees - self.fees_paid
        super().save(*args, **kwargs)


class ExamFee(models.Model):
    class Meta:
        db_table = 'ExamFee'

    student = models.ForeignKey('StudentsPry', on_delete=models.CASCADE, related_name='exam_fee', db_index=True)
    term = models.ForeignKey('AcademicCalender', on_delete=models.CASCADE, db_index=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    outstanding_balance = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.outstanding_balance = self.fee - self.paid
        super().save(*args, **kwargs)
    
    
    
class VacationFee(models.Model):
    class Meta:
        db_table = 'VacationFee'

    student = models.ForeignKey('StudentsPry', on_delete=models.CASCADE, related_name='vacation_fee', db_index=True)
    term = models.ForeignKey('AcademicCalender', limit_choices_to={'term__in': ['Holyday April', 'Holyday August', 'Holyday December']}, on_delete=models.CASCADE, db_index=True)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    outstanding_balance = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        previous_term_fees = VacationFee.objects.filter(student=self.student, term__id__lt=self.term.id).last()
        if previous_term_fees:
            self.opening_balance = previous_term_fees.outstanding_balance
        self.fee = self.opening_balance + self.term.fees
        self.outstanding_balance = self.fee - self.paid
        super().save(*args, **kwargs)



class TripsFee(models.Model):
    class Meta:
        db_table = 'TripsFee'

    student = models.ForeignKey('StudentsPry', on_delete=models.CASCADE, related_name='trips_fee', db_index=True)
    term = models.ForeignKey('AcademicCalender', on_delete=models.CASCADE, db_index=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    outstanding_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.outstanding_balance = self.fee - self.paid
        super().save(*args, **kwargs)



class Payments(models.Model):
    class Meta:
        db_table = 'Payments'

    student = models.ForeignKey('StudentsPry', on_delete=models.CASCADE, related_name='payments')
    term = models.ForeignKey('AcademicCalender', on_delete=models.CASCADE)
    purpose = models.CharField(max_length=20, choices=[
        ('Fees', 'Fees'),
        ('Trips Fee', 'Trips Fee'),
        ('Vacation Fee', 'Vacation Fee'),
        ('Exam Fee', 'Exam Fee')
    ])
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    fee = GenericForeignKey('content_type', 'object_id')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        fee = self.fee
        if isinstance(fee, Fees):
            fee.fees_paid += self.amount
            fee.outstanding_balance = fee.total_fees - fee.fees_paid
            fee.save()
        elif isinstance(fee, ExamFee):
            fee.paid += self.amount
            fee.outstanding_balance = fee.fee - fee.paid
            fee.save()
        elif isinstance(fee, VacationFee):
            fee.paid += self.amount
            fee.outstanding_balance = fee.fee - fee.paid
            fee.save()
        elif isinstance(fee, TripsFee):
            fee.paid += self.amount
            fee.outstanding_balance = fee.fee - fee.paid
            fee.save()
        super().save(*args, **kwargs)
        
        
class OverallFeesStructure(models.Model):
    class Meta:
        db_table = 'OverallFeesStructure'
        unique_together = ('student', 'term')

    student = models.ForeignKey('StudentsPry', on_delete=models.CASCADE, related_name='overall_fees', db_index=True)
    term = models.ForeignKey('AcademicCalender', on_delete=models.CASCADE, db_index=True)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    total_outstanding = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        fees = Fees.objects.filter(student=self.student, term=self.term).last()
        exam_fee = ExamFee.objects.filter(student=self.student, term=self.term).last()
        vacation_fee = VacationFee.objects.filter(student=self.student, term=self.term).last()
        trips_fee = TripsFee.objects.filter(student=self.student, term=self.term).last()

        self.total_fees = (fees.total_fees if fees else 0) + \
                         (exam_fee.fee if exam_fee else 0) + \
                         (vacation_fee.fee if vacation_fee else 0) + \
                         (trips_fee.fee if trips_fee else 0)

        self.total_paid = (fees.fees_paid if fees else 0) + \
                          (exam_fee.paid if exam_fee else 0) + \
                          (vacation_fee.paid if vacation_fee else 0) + \
                          (trips_fee.paid if trips_fee else 0)

        self.total_outstanding = (fees.outstanding_balance if fees else 0) + \
                                 (exam_fee.outstanding_balance if exam_fee else 0) + \
                                 (vacation_fee.outstanding_balance if vacation_fee else 0) + \
                                 (trips_fee.outstanding_balance if trips_fee else 0)

        super().save(*args, **kwargs)
        
        
        