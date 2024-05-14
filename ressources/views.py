from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import Course, Subject, Year, Chapter, TD, TP, Homework, Note, Quiz, Forum, Post, Comment
from .serializers import (CourseSerializer, SubjectSerializer, ChapterSerializer, 
                          TDSerializer, TeacherSubjectsSerializer, TPSerializer,
                          NoteSerializer, HomeworkSerializer, CourseUploadSerializer,
                          QuizSerializer, ForumSerializer, PostSerializer, CommentSerializer,
                          TeacherSubjectsPerYearSerializer)
from rest_framework import generics, permissions, authentication
from profiles.permissions import IsEditorTeacherPermission, isTeacherPermission, IsStaffPermission, IsEditorTeacherOrAdminPermission
from profiles.models import Teacher, User, Student
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.parsers import FileUploadParser
from .permissions import IsAccountOwnerPermission
import os
# Create your views here.


class SubjectsRetriveView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    lookup_field = 'id'    
    
class SubjectsListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
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
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        queryset = Chapter.objects.filter(subject=id)
        serializer = ChapterSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')
        chapter_name = request.data.get('chapter_name')
        chapter_desc = request.data.get('chapter_desc') or ""
        chapter = Chapter.objects.create(subject=Subject.objects.get(id=id), name=chapter_name, description=chapter_desc)
        chapter.save()
        return Response({'response': "Chapter has been added"}, status=status.HTTP_201_CREATED)

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
    
    def post(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        title = request.data.get('title')
        description = request.data.get('description') or ""
        print(request.FILES)
        content = request.FILES.get('content')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        course = Course.objects.create(chapter=chapter, title=title, description=description, content=content)
        return Response({'details': 'course created'}, status=status.HTTP_201_CREATED)
class ChapterCourseDeleteView(APIView):
    
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        number = kwargs.get('cours')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            queryset = Course.objects.get(chapter=chapter, number=number)
        except Course.DoesNotExist:
            return Response({'details': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)# print(queryset)
        serializer = CourseSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        cours = kwargs.get('cours')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            course = Course.objects.get(chapter=chapter, number=cours)
        except Course.DoesNotExist:
            return Response({'details': 'course not found'}, status=status.HTTP_404_NOT_FOUND)
        print(course)
        course.delete()
        return Response({'details': 'course deleted'}, status=status.HTTP_204_NO_CONTENT)
    
class ChapterTDDeleteView(APIView):
    
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        number = kwargs.get('td')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            queryset = TD.objects.get(chapter=chapter, number=number)
        except TD.DoesNotExist:
            return Response({'details': 'TD not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TDSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        number = kwargs.get('td')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            td = TD.objects.get(chapter=chapter, number=number)
        except TD.DoesNotExist:
            return Response({'details': 'TD not found'}, status=status.HTTP_404_NOT_FOUND)
        td.delete()
        return Response({'details': 'TD deleted'}, status=status.HTTP_204_NO_CONTENT)
    
class ChapterTPDeleteView(APIView):
    
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        number = kwargs.get('tp')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            queryset = TP.objects.get(chapter=chapter, number=number)
        except TP.DoesNotExist:
            return Response({'details': 'TP not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TPSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        number = kwargs.get('tp')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            tp = TP.objects.get(chapter=chapter, number=number)
        except TD.DoesNotExist:
            return Response({'details': 'TP not found'}, status=status.HTTP_404_NOT_FOUND)
        tp.delete()
        return Response({'details': 'TP deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    
class ChapterHomeworkDeleteView(APIView):
    
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        number = kwargs.get('homework')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            queryset = Homework.objects.get(chapter=chapter, number=number)
        except Homework.DoesNotExist:
            return Response({'details': 'Homework not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = HomeworkSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        number = kwargs.get('homework')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            homework = Homework.objects.get(chapter=chapter, number=number)
        except Homework.DoesNotExist:
            return Response({'details': 'Homework not found'}, status=status.HTTP_404_NOT_FOUND)
        homework.delete()
        return Response({'details': 'Homework deleted'}, status=status.HTTP_204_NO_CONTENT)
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

class CoursesView(generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseUploadSerializer
    # permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'
    # parser_classes = [FileUploadParser]
    
    # def post(self, request, *args, **kwargs):
    #     file = request.data['file']
        

class CoursesDeleteView(generics.DestroyAPIView, generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'id'    
    # permission_classes = [permissions.IsAdminUser]
    
    
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
    
    def post(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        title = request.data.get('title')
        description = request.data.get('description') or ""
        content = request.FILES.get('content')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        td = TD.objects.create(chapter=chapter, title=title, description=description, content=content)
        return Response({'details': 'TD created'}, status=status.HTTP_201_CREATED)
    
class TPRetrieveView(APIView):
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        queryset = TP.objects.filter(chapter=chapter)
        serializer = TPSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        title = request.data.get('title')
        description = request.data.get('description') or ""
        content = request.FILES.get('content')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        tp = TP.objects.create(chapter=chapter, title=title, description=description, content=content)
        return Response({'details': 'TP created'}, status=status.HTTP_201_CREATED)
    
class HomeworkRetrieveView(APIView):
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        queryset = Homework.objects.filter(chapter=chapter)
        serializer = HomeworkSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        title = request.data.get('title')
        deadline = request.data.get('deadline')
        description = request.data.get('description') or ""
        content = request.FILES.get('content')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        homework = Homework.objects.create(chapter=chapter, title=title, description=description, content=content, deadline=deadline)
        return Response({'details': 'homework created'}, status=status.HTTP_201_CREATED)
    
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
    
class SubjectHomeworkListView(APIView):
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        try:
            subject = Subject.objects.get(id=subject)
        except Subject.DoesNotExist:
            return Response({'details': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
        chapters = Chapter.objects.filter(subject=subject)
        queryset = Homework.objects.filter(chapter__in=chapters)
        serializer = HomeworkSerializer(queryset, many=True)
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
    
class TeacherSubjectView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            teacher_id = kwargs.get('teacher')
            teacher = Teacher.objects.get(pk=teacher_id)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=404)
        
        serializer = TeacherSubjectsPerYearSerializer(teacher,)
        return Response(serializer.data)

class NoteRetrieveView(APIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAccountOwnerPermission]
    
    def get(self, request, *args, **kwargs):
        student = kwargs.get('student')
        subject = kwargs.get('subject')
        student = get_object_or_404(Student, id=student)
        subject = Subject.objects.get(id=subject)
        note, _ = Note.objects.get_or_create(owner=student, subject=subject)
        self.check_object_permissions(request, note)
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, *args, **kwargs):
        student = kwargs.get('student')
        subject = kwargs.get('subject')
        student = get_object_or_404(Student, id=student)
        subject = Subject.objects.get(id=subject)
        note, _ = Note.objects.get_or_create(owner=student, subject=subject)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class SubjectQuizListView(APIView):
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        try:
            subject = Subject.objects.get(id=subject)
        except Subject.DoesNotExist:
            return Response({'details': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
        chapters = Chapter.objects.filter(subject=subject)
        queryset = Quiz.objects.filter(chapter__in=chapters)
        serializer = QuizSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class QuizRetrieveView(APIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        chapter = kwargs.get('chapter')
        try:
            chapter = Chapter.objects.get(subject=subject, number=chapter)
        except Chapter.DoesNotExist:
            return Response({'details': 'chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        queryset = Quiz.objects.filter(chapter=chapter)
        serializer = QuizSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ForumPostListView(APIView):
    def get(self, request, *args, **kwargs):
        subject = kwargs.get('subject')
        try:
            subject = Subject.objects.get(id=subject)
        except Subject.DoesNotExist:
            return Response({'details': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            forum = Forum.objects.get(subject=subject)
        except Forum.DoesNotExist:
            return Response({'details': "forum not found"}, status=status.HTTP_404_NOT_FOUND)
        queryset = Post.objects.filter(forum=forum)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PostCommentListView(APIView):
    def get(self, request, *args, **kwargs):
        post = kwargs.get('post')
        try:
            post = Post.objects.get(id=post)
        except Post.DoesNotExist:
            return Response({'details': 'post not found'}, status=status.HTTP_404_NOT_FOUND)
        queryset = Comment.objects.filter(post=post)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)