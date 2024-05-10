from rest_framework import serializers
from .models import Course, Subject, Chapter, TD, TP, Note, Homework, Quiz, Question, Answer
from profiles.models import Teacher
from profiles.serializers import UserSerializer
class CourseSerializer(serializers.ModelSerializer):
    chapter_tag = serializers.IntegerField(source='chapter.number', read_only=True)
    class Meta:
        model = Course
        fields = '__all__'
        
    def create(self, validated_data):
        if not validated_data.get('description'):
            validated_data['description'] = 'Aucune description'
        
        return super().create(validated_data)
    
class TDSerializer(serializers.ModelSerializer):
    chapter_tag = serializers.IntegerField(source='chapter.number', read_only=True)
    class Meta:
        model = TD
        fields = '__all__'
        
class HomeworkSerializer(serializers.ModelSerializer):
    chapter_tag = serializers.IntegerField(source='chapter.number', read_only=True)
    class Meta:
        model = Homework
        fields = '__all__'
        
class TPSerializer(serializers.ModelSerializer):
    chapter_tag = serializers.IntegerField(source='chapter.number', read_only=True)
    class Meta:
        model = TP
        fields = '__all__'
class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'
class SubjectSerializer(serializers.ModelSerializer):
    
    teacher_name = serializers.CharField(source='main_teacher.user', read_only=True)
    teacher_email = serializers.CharField(source='main_teacher.user.email', read_only=True)
    teacher_degree = serializers.CharField(source='main_teacher.degree', read_only=True)
    class Meta:
        model = Subject
        fields = '__all__'
    def create(self, validated_data):
        if not validated_data.get('description'):
            validated_data['description'] = 'Aucune description'
        
        return super().create(validated_data)
        
class TeacherSubjectsSerializer(serializers.ModelSerializer):
    year_number = serializers.IntegerField(source='year.year', read_only=True)
    class Meta:
        model = Subject
        fields = '__all__'
class YearSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        
class NoteSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='owner', read_only=True)
    subject_name = serializers.CharField(source='subject', read_only=True)
    class Meta:
        model = Note
        fields = '__all__'
        
        
class QuizSerializer(serializers.ModelSerializer):
    chapter_tag = serializers.IntegerField(source='chapter.number', read_only=True)
    
    class Meta:
        model = Quiz
        fields = '__all__'
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'