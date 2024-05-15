from rest_framework import serializers
from .models import (Course, Subject, Chapter,
                     TD, TP, Note, Homework,
                     Quiz, Question, Answer,
                     Forum, Post, Comment, Other,
                     News)
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
    comments = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    votes = serializers.SerializerMethodField()
    # subject = serializers.CharField(source='forum.subject', read_only=True)
    # comments = serializers.CharField(source='comments', read_only=True)
    
    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj)
        return CommentSerializer(comments, many=True).data
    
    def get_comment_count(self, obj):
        comments = Comment.objects.filter(post=obj)
        return comments.count()

    def get_votes(self, obj):
        upvotes = obj.get_votes
        return upvotes
    class Meta:
        model = Post
        fields = '__all__'
        
class PostVoteSerializer(serializers.ModelSerializer):
    
    votes = serializers.SerializerMethodField()
    
    def get_votes(self, obj):
        votes = obj.get_votes
        return votes
    class Meta:
        model = Post
        fields = ['id', 'title', 'upvotes', 'downvotes', 'votes']
        
class ForumPostsSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject', read_only=True)
    posts = serializers.SerializerMethodField()
    
    def get_posts(self, obj):
        posts = Post.objects.filter(forum=obj)
        return PostSerializer(posts, many=True).data
    
    class Meta:
        model = Forum
        fields = '__all__'
class CommentSerializer(serializers.ModelSerializer):
    op_name = serializers.CharField(source='post.author', read_only=True)
    commenter_name = serializers.CharField(source='author', read_only=True)
    og_post_title = serializers.CharField(source='post.title', read_only=True)
    votes = serializers.SerializerMethodField()
    
    
    def get_votes(self, obj):
        return obj.get_votes
    class Meta:
        model = Comment
        fields = '__all__'
        
class OtherSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='chapter.subject', read_only=True)
    class Meta:
        model = Other
        fields = '__all__'
        
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'