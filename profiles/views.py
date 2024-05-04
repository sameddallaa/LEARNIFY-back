from django.contrib.auth import authenticate, update_session_auth_hash
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError
from rest_framework import generics, status, permissions, authentication
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from .tokens import create_token_pair_for_user
from .models import Student, Teacher, User, Year, Group
from .serializers import SignupSerializer, StudentSerializer, TeacherSerializer, UserSerializer, UploadedFileSerializer, ChangePasswordSerializer, MyTokenObtainPairSerializer, YearSerializer, GroupSerializer, TeacherYearsSerializer
from .permissions import IsAccountOwnerPermission
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
import csv
from .utils import generate_password, send_password_after_signup, find_among_users
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
import uuid
from ressources.models import Subject
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
            group = self.request.data.get('group')
            student_profile.year = year
            student_profile.group = group
            student_profile.save()

        elif user.is_teacher:
            teacher_profile = Teacher.objects.get(user=user)
            degree = self.request.data.get('degree')
            teacher_profile.degree = degree
            teacher_profile.save()
            
def make_username(firstname: str, lastname: str):
    default = firstname[0] + '.' + lastname
    # username = firstname[0] + '.' + lastname
    if not User.objects.filter(username=default).exists():
        return (default + str(uuid.uuid4())[0:4]).lower()
    
    # username = default + uuid.uuid4()[0:4]
    
    # return username.lower()
# @csrf_exempt
class FileUploadStudentsAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            users = []
            file = serializer.validated_data['file']
            file_content = file.read().decode('utf-8').splitlines()
            students = csv.reader(file_content)
            next(students)
            unsuccessful_attempts = []
            for student in students:
                if not User.objects.filter(email=student[0]).exists():
                    users.append({
                        'email': student[0],
                        'username': student[1][0] + '.' + student[2],
                        'first_name': student[1],
                        'last_name': student[2],
                        'group': student[3],
                        'year': student[4],
                        'password': generate_password(12),
                        'is_student': True,
                        'is_staff': False,
                        'is_teacher': False,
                        # 'is_editor_teacher': False,
                    })
                else:
                    unsuccessful_attempts.append({
                        'email': student[0],
                        # 'username': student[1] + student[2],
                        'first_name': student[1],
                        'last_name': student[2],
                        'group': student[3],
                        'year': student[4],
                        'is_student': True,
                        'is_staff': False,
                        'is_teacher': False,
                        # 'is_editor_teacher': False,
                    })
            with transaction.atomic():
                
                created_users = User.objects.bulk_create([
                    User(
                        email=user['email'],
                        username=user['username'],
                        first_name=user['first_name'],
                        last_name=user['last_name'],
                        password=make_password(user['password']),
                        is_student=True
                    )
                    for user in users
                ], batch_size=1000, ignore_conflicts=True)
                for created_user, user in zip(created_users, users):
                    student = Student.objects.get(user=created_user)
                    student.save(year=user['year'], group=user['group'])
                    
                    # user = find_among_users(users, 'email', created_user.email)
                    # password = user['password']
                    # user = User.objects.get(email=user['email'])
                    
                    # send_password_after_signup(password, user)
            if unsuccessful_attempts:
                return Response({'message': "Some student were not added successfully.", 'unsuccessful_attempts': unsuccessful_attempts}, status=status.HTTP_207_MULTI_STATUS)
            return Response({'success': 'Students were added successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid file'}, status=status.HTTP_400_BAD_REQUEST)
    
#
# @csrf_exempt
class FileUploadTeacherAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAdminUser]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            users = []
            file = serializer.validated_data['file']
            file_content = file.read().decode('utf-8').splitlines()
            teachers = csv.reader(file_content)
            next(teachers)
            unsuccessful_attempts = []
            for teacher in teachers:
                if not (User.objects.filter(email=teacher[0]).exists() or User.objects.filter(username=teacher[1] + teacher[2])):
                    users.append({
                        'email': teacher[0],
                        'username': teacher[1][0] + "." + teacher[2],
                        'first_name': teacher[1],
                        'last_name': teacher[2],
                        'degree': teacher[3],
                        # 'is_editor_teacher': teacher[4],
                        'password': generate_password(12),
                        'is_student': False,
                        'is_staff': False,
                        'is_teacher': True,
                        # 'is_editor_teacher': teacher[4] == "éditeur",
                    })
                else:
                    unsuccessful_attempts.append({
                        'email': teacher[0],
                        # 'username': teacher[1] + teacher[2],
                        'first_name': teacher[1],
                        'last_name': teacher[2],
                        'degree': teacher[3],
                        # 'year': teacher[4],
                        'is_student': False,
                        'is_staff': False,
                        'is_teacher': True,
                        # 'is_editor_teacher': False,
                    })
            with transaction.atomic():
                
                created_users = User.objects.bulk_create([
                    User(
                        email=user['email'],
                        username=user['username'],
                        first_name=user['first_name'],
                        last_name=user['last_name'],
                        password=make_password(user['password']),
                        is_teacher=True
                    )
                    for user in users
                ], batch_size=1000, ignore_conflicts=True)
                
                
                for created_user, user in zip(created_users, users):
                    teacher = Teacher.objects.get(user=created_user)
                    teacher.degree = user['degree']
                    teacher.save()
                    
                    # user = find_among_users(users, 'email', created_user.email)
                    # password = user['password']
                    # user = User.objects.get(email=user['email'])
                    
                    # send_password_after_signup(password, user)
            if unsuccessful_attempts:
                return Response({'message': "Some teacher were not added successfully.", 'unsuccessful_attempts': unsuccessful_attempts}, status=status.HTTP_207_MULTI_STATUS)
            return Response({'success': 'Teachers were added successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid file'}, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]
    def get(self, request, *args, **kwargs):
        obj = {
            'user': str(request.user),
            'auth': str(request.auth)
        }

        return Response(data=obj, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            tokens = create_token_pair_for_user(user)
            obj = {
                'message': 'Login successful',
                'tokens': tokens
            }

            return Response(data=obj, status=status.HTTP_200_OK)
        return Response(data={
            'message': 'Email or password incorrect',
        }, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

class ChangePasswordView(generics.UpdateAPIView):
    
    permission_classes = [IsAccountOwnerPermission]
    serializer_class = ChangePasswordSerializer
    def get_object(self):
        obj = self.request.user
        return obj
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            update_session_auth_hash(request, request.user)

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
    
class TeacherRetrieveView(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    
class YearListView(ListAPIView):
    queryset = Year.objects.all()
    serializer_class = YearSerializer
    permission_classes = [permissions.AllowAny]
    
class GroupListView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]
    
    
class TeachersYearsView(APIView):
    def get(self, request, *args, **kwargs):
        teacher = kwargs.get('teacher')
        # teacher = Teacher.objects.filter(id=teacher).first()
        # print(teacher)
        subjects = Subject.objects.filter(teachers=teacher)
        years = subjects.values_list('year', flat=True)
        years = Year.objects.filter(id__in=years)
        serializer = YearSerializer(years, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)