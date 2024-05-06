from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import Course, Subject, Year, Chapter, TD, TP
from .serializers import CourseSerializer, SubjectSerializer, ChapterSerializer, TDSerializer, TeacherSubjectsSerializer, TPSerializer
from rest_framework import generics, permissions, authentication
from profiles.permissions import IsEditorTeacherPermission, isTeacherPermission, IsStaffPermission, IsEditorTeacherOrAdminPermission
from profiles.models import Teacher
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
# Create your views here.


class SubjectsRetriveView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    lookup_field = 'id'    
    
class SubjectsListView(generics.ListAPIView):
    # lookup_field = 'year'
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    # authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication,]
    permission_classes = [permissions.IsAdminUser]

class SubjectsCreateView(generics.CreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectsUpdateView(generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    lookup_field = 'id'
    
class SubjectYearView(APIView):
    def get(self, request, *args, **kwargs):
        year = kwargs.get('year')
        queryset = Subject.objects.filter(year=Year.objects.get(year=year))
        serializer = SubjectSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ChapterView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        queryset = Chapter.objects.filter(subject=id)
        serializer = ChapterSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class SubjectsDeleteView(generics.DestroyAPIView, generics.RetrieveAPIView):
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializer
#     lookup_field = 'id'
    
class CoursesRetriveView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'
    
    
class ChapterCourseRetrieveView(APIView):
        def get(self, request, *args, **kwargs):
            subject = kwargs.get('subject')
            chapter = kwargs.get('chapter')
            try:
                chapter = Chapter.objects.get(subject=subject, number=chapter)
            except Chapter.DoesNotExist:
                return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
            queryset = Course.objects.filter(chapter=chapter)
            # print(queryset)
            serializer = CourseSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
class CourseRetrieveView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if not Course.objects.filter(id=id).exists():
            return Response(data={'error': 'Course could not be found'}, status=status.HTTP_404_NOT_FOUND)
        course = Course.objects.get(id=id)
        course_path = str(course.content)
        print(os.path.join(settings.MEDIA_ROOT, course_path))
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, course_path)):
            print(f"i'm the path {course_path}")
            return Response(data={'error': 'File could not be found'}, status=status.HTTP_404_NOT_FOUND)
        file_name = os.path.basename(course_path)
        course_path = os.path.join(settings.MEDIA_ROOT)
        return FileResponse(open(course_path, 'r'), as_attachment=True, filename=file_name)
class CoursesListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CoursesCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAdminUser]

class CoursesUpdateView(generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'

class CoursesDeleteView(generics.DestroyAPIView, generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'id'    
    permission_classes = [permissions.IsAdminUser]
    
    
class TDRetrieveView(APIView):
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        queryset = TD.objects.filter(chapter=chapter)
        # print(queryset)
        serializer = TDSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TPRetrieveView(APIView):
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        queryset = TP.objects.filter(chapter=chapter)
        # print(queryset)
        serializer = TPSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class SubjectCourseListView(APIView):
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        try:
            subject = Subject.objects.get(id=subject)
        except Subject.DoesNotExist:
            return Response({'details': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
        chapters = Chapter.objects.filter(subject=subject)
        queryset = Course.objects.filter(chapter__in=chapters)
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class SubjectTDListView(APIView):
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        try:
            subject = Subject.objects.get(id=subject)
        except Subject.DoesNotExist:
            return Response({'details': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
        chapters = Chapter.objects.filter(subject=subject)
        queryset = TD.objects.filter(chapter__in=chapters)
        serializer = TDSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SubjectTPListView(APIView):
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        try:
            subject = Subject.objects.get(id=subject)
        except Subject.DoesNotExist:
            return Response({'details': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
        chapters = Chapter.objects.filter(subject=subject)
        queryset = TP.objects.filter(chapter__in=chapters)
        serializer = TPSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TeacherSubjectsView(APIView):
    def get(self, request, *args, **kwargs):
        teacher = kwargs.get('teacher')
        teacher = Teacher.objects.filter(id=teacher).first()
        subjects = Subject.objects.filter(teachers=teacher)
        serializer = TeacherSubjectsSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TeacherSubjectPerYearView(APIView):
    def get (self, request, *args, **kwargs):
        year = kwargs.get('year')
        teacher = kwargs.get('teacher')
        queryset = Subject.objects.filter(year=Year.objects.get(year=year), teachers=teacher)
        serializer = SubjectSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)