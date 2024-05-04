from rest_framework import serializers
from .models import Course, Subject, Chapter, TD
from profiles.models import Teacher

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        
    def create(self, validated_data):
        if not validated_data.get('description'):
            validated_data['description'] = 'Aucune description'
        
        return super().create(validated_data)
    
class TDSerializer(serializers.ModelSerializer):
    class Meta:
        model = TD
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