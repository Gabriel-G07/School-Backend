import uuid
from Admin_app.models import StudentsPry
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.db.models.signals import post_save
from django.dispatch import receiver


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsPry
        fields = '__all__'

