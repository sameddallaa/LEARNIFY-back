from django.shortcuts import render
from .models import Course, Subject, Year
from .serializers import CourseSerializer, SubjectSerializer
from rest_framework import generics, permissions, authentication
from profiles.permissions import IsEditorTeacherPermission, isTeacherPermission, IsStaffPermission, IsEditorTeacherOrAdminPermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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

# class SubjectsDeleteView(generics.DestroyAPIView, generics.RetrieveAPIView):
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializer
#     lookup_field = 'id'
    
class CoursesRetriveView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [isTeacherPermission]
    lookup_field = 'id'    
    
class CoursesListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CoursesCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsEditorTeacherPermission]

class CoursesUpdateView(generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsEditorTeacherPermission]
    lookup_field = 'id'

class CoursesDeleteView(generics.DestroyAPIView, generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'id'    
    permission_classes = [IsEditorTeacherOrAdminPermission]