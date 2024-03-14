from rest_framework import serializers
from .models import Profile, Student, Teacher

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'