from rest_framework import serializers
from .models import Course, Subject, Chapter, TD, TP, Note, Homework, Quiz, Question, Answer, Forum, Post, Comment, Other
from profiles.models import Teacher, Year
from profiles.serializers import UserSerializer, YearSerializer
class CourseSerializer(serializers.ModelSerializer):
    chapter_tag = serializers.IntegerField(source='chapter.number', read_only=True)
    class Meta:
        model = Course
        fields = '__all__'
        
    def create(self, validated_data):
        if not validated_data.get('description'):
            validated_data['description'] = 'Aucune description'
        
        return super().create(validated_data)
    
    
class CourseUploadSerializer(serializers.ModelSerializer):
    content = serializers.FileField()
    class Meta:
        model = Course
        fields = '__all__'
    
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
        
        
class TeacherSubjectsPerYearSerializer(serializers.ModelSerializer):
    years_subjects = serializers.SerializerMethodField()
    # subjects = serializers.SerializerMethodField()
    
    def get_years_subjects(self, obj):
        years = Subject.objects.filter(teachers=obj).distinct().values_list('year')
        # years = Year.objects.filter(pk__in=years)
        subjects = []
        for year in years:
            subjects.append({'year': YearSerializer(Year.objects.get(pk=year[0])).data, 
                             'subjects': SubjectSerializer(Subject.objects.filter(year=year, teachers=obj), many=True).data})
        return subjects
    # def get_subjects(self, obj):
    #     subjects = Subject.objects.filter(teachers=obj)
    #     subjects_serialized = SubjectSerializer(subjects, many=True).data
    #     years = Year.objects.values_list('year', flat=True)
    #     years_serialized = YearSerializer(years, many=True).data
    #     data = [{
    #         'year': year,
    #         'subjects': [subject for subject in subjects_serialized]
    #     } for year in years_serialized]
    #     return data
    class Meta:
        model = Teacher
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
        
        
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    chapter_tag = serializers.IntegerField(source='chapter.number', read_only=True)
    class Meta:
        model = Quiz
        fields = '__all__'
        
class ForumSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject', read_only=True)
    class Meta:
        model = Forum
        fields = '__all__'
        
        
class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author', read_only=True)
    subject = serializers.CharField(source='forum.subject', read_only=True)
    # comments = serializers.CharField(source='comments', read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='post.author', read_only=True)
    commenter_name = serializers.CharField(source='author', read_only=True)
    og_post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'
        
class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Other
        fields = '__all__'