from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status, permissions, authentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .users import User
from .tokens import create_token_pair_for_user
from .models import Student, Teacher
from .serializers import SignupSerializer, StudentSerializer, TeacherSerializer, UserSerializer
from rest_framework.views import APIView


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
            # token, created = Token.objects.get_or_create(user=user)
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
    permission_classes = [permissions.AllowAny]

class StudentListView(ListAPIView):
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
class TeacherListView(ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer