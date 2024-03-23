from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from .tokens import create_token_pair_for_user
from .models import Student, Teacher, User
from .serializers import SignupSerializer, StudentSerializer, TeacherSerializer, UserSerializer, UploadedFileSerializer
from rest_framework.views import APIView
import csv

class SignupView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user = serializer.save()
        if user.is_student:
            student_profile = Student.objects.get(user=user)
            year = self.request.data.get('year')
            major = self.request.data.get('major')
            student_profile.year = year
            student_profile.major = major
            student_profile.save()

        elif user.is_teacher:
            teacher_profile = Teacher.objects.get(user=user)
            degree = self.request.data.get('degree')
            teacher_profile.degree = degree
            teacher_profile.save()
            
            
            
class FileUploadAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAdminUser]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            users = []
            file = serializer.validated_data['file']
            file_content = file.read().decode('utf-8').splitlines()
            print(file_content)
            students = csv.reader(file_content)
            next(students)
            user = []
            for student in students:
                users.append({
                    'email': student[0],
                    'username': student[1] + student[2],
                    'first_name': student[1],
                    'last_name': student[2],
                    'major': student[3],
                    'year': student[4],
                    'password':'student password',
                    'is_student': True,
                    'is_staff': False,
                    'is_teacher': False,
                    'is_editor_teacher': False,
                })
            
            for user in users:
                User.objects.create_student(
                    user['email'], 
                    user['username'],
                    user['first_name'],
                    user['last_name'],
                    user['major'],
                    user['year'],
                    user['password'], 
                )
                
            return Response({'success': "Students added successfully."}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid file'}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        obj = {
            'user': str(request.user),
            'auth': str(request.auth)
        }

        return Response(data=obj, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            tokens = create_token_pair_for_user(user)
            obj = {
                'message': 'Login successful',
                'token': tokens
            }

            return Response(data=obj, status=status.HTTP_200_OK)
        return Response(data={
            'message': 'Email or password incorrect',
        }, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class StudentListView(ListAPIView):
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
class TeacherListView(ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer