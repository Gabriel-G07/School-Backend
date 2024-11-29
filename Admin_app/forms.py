from django import forms
from .models import *

class StudentEnrolmentForm(forms.ModelForm):
    class Meta:
        model = StudentsEnrolmentsPry
        fields = ['name', 'surname', 'Gender', 'dob', 'email', 'Grade_Level', 'country', 'city', 'area', 'street', 'house_number', 'Phone_Number', 'Parent_name', 'Parent_surname', 'Parent_Email', 'Relationship', 'Parent_Phone_Number']
        labels = {
            'name': 'Name',
            'surname': 'Surname',
            'Gender': 'Gender',
            'dob': 'Date of Birth',
            'email': 'Email',
            'Phone_Number': 'Phone Number',
            'Grade_Level': 'Grade Level',
            'country':'Country',
            'city':'City',
            'area':'Area',
            'street':'Street',
            'house_number':'house_number',
            'Parent_name': 'Parent/Guardian name',
            'Parent_surname': 'Parent/Guardian surname',
            'Parent_Email': 'Parent/Guardian Email',
            'Relationship': 'Your Relationship',
            'Parent_Phone_Number': 'Parent/Guardian Phone Number',
        }
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }


class JobApplicationsForm(forms.ModelForm):
    class Meta:
        model = JobApplications
        fields = ['name', 'surname', 'Gender', 'pPosition', 'dob', 'Marital_Status', 'email', 'country', 'city', 'area', 'street', 'house_number', 'PhoneNumber']
        labels = {
            'name': 'Name',
            'surname': 'Surname',
            'Gender': 'Gender',
            'pPosition': 'Prospactive Position',
            'dob': 'Date of Birth',
            'Marital_Status': 'Marital Status',
            'email': 'Email',
            'PhoneNumber': 'PhoneNumber',
            'country':'Country',
            'city':'City',
            'area':'Area',
            'street':'Street',
            'house_number':'house_number',
        }
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }