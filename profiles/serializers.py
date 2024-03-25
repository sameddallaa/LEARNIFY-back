from rest_framework.validators import ValidationError
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Student, Teacher, UploadedFile, User

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=511, default=str(first_name)+str(last_name))
    password = serializers.CharField(min_length=8, write_only=True)
    is_student = serializers.BooleanField(default=True)
    is_teacher = serializers.BooleanField(default=False)
    is_editor_teacher = serializers.BooleanField(default=False)
    is_staff = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'is_student', 'is_teacher', 'is_editor_teacher', 'is_staff']
        
    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            raise ValidationError('Email already exists')
        if User.objects.filter(username=attrs.get('username')).exists():
            raise ValidationError('Username already exists')
        has_multiple_roles = not (attrs.get('is_student') ^ attrs.get('is_teacher') ^ attrs.get('is_staff'))
        if has_multiple_roles:
            raise ValidationError('You must select only one role')
        if attrs.get('is_editor_teacher') and not attrs.get('is_teacher'):
            raise ValidationError('You must select is_teacher if you select is_editor_teacher')
        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data['password']
        user = super().create(validated_data)
        user.set_password(password)
        is_teacher, is_editor_teacher = validated_data['is_teacher'], validated_data['is_editor_teacher']
        if is_editor_teacher and not is_teacher:
            validated_data['is_teacher'] = True
        user.save()
        Token.objects.create(user=user)
        return user
    
    
class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'
        
        
class ChangePasswordSerializer(serializers.Serializer):
    model = User
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True) 
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'    

class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = '__all__'
        
class TeacherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Teacher
        fields = '__all__'