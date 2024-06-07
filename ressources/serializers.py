from rest_framework import serializers
from .models import (
    Course,
    Subject,
    Chapter,
    TD,
    TP,
    Note,
    Homework,
    Quiz,
    Question,
    Answer,
    Forum,
    Post,
    Comment,
    Other,
    News,
)
from profiles.models import Teacher, Year, Student
from profiles.serializers import (
    UserSerializer,
    YearSerializer,
    TeacherSerializer,
    StudentSerializer,
)
from django.utils import timezone


class CourseSerializer(serializers.ModelSerializer):
    chapter_tag = serializers.IntegerField(source="chapter.number", read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def create(self, validated_data):
        if not validated_data.get("description"):
            validated_data["description"] = "Aucune description"

        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)
        if not representation["content"].startswith("http://localhost:8000"):
            representation["content"] = (
                "http://localhost:8000" + representation["content"]
            )
        return representation


class CourseUploadSerializer(serializers.ModelSerializer):
    content = serializers.FileField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)
        if not representation["content"].startswith("http://localhost:8000"):
            representation["content"] = (
                "http://localhost:8000" + representation["content"]
            )
        return representation

    class Meta:
        model = Course
        fields = "__all__"


class TDSerializer(serializers.ModelSerializer):
    chapter_tag = serializers.IntegerField(source="chapter.number", read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)
        if not representation["content"].startswith("http://localhost:8000"):
            representation["content"] = (
                "http://localhost:8000" + representation["content"]
            )
        return representation

    class Meta:
        model = TD
        fields = "__all__"


class HomeworkSerializer(serializers.ModelSerializer):
    chapter_tag = serializers.IntegerField(source="chapter.number", read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation["content"].startswith("http://localhost:8000"):
            representation["content"] = (
                "http://localhost:8000" + representation["content"]
            )
        return representation

    class Meta:
        model = Homework
        fields = "__all__"


class TPSerializer(serializers.ModelSerializer):
    chapter_tag = serializers.IntegerField(source="chapter.number", read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation["content"].startswith("http://localhost:8000"):
            representation["content"] = (
                "http://localhost:8000" + representation["content"]
            )
        return representation

    class Meta:
        model = TP
        fields = "__all__"


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):

    teacher_name = serializers.CharField(source="main_teacher.user", read_only=True)
    teacher_email = serializers.CharField(
        source="main_teacher.user.email", read_only=True
    )
    teacher_degree = serializers.CharField(source="main_teacher.degree", read_only=True)
    teachers = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = "__all__"

    def get_teachers(self, obj):
        teachers = []
        for teacher in obj.teachers.all():
            teachers.append(TeacherSerializer(teacher).data)
        return teachers

    def create(self, validated_data):
        if not validated_data.get("description"):
            validated_data["description"] = "Aucune description"

        return super().create(validated_data)


class TeacherSubjectsSerializer(serializers.ModelSerializer):
    year_number = serializers.IntegerField(source="year.year", read_only=True)

    class Meta:
        model = Subject
        fields = "__all__"


class TeacherSubjectsPerYearSerializer(serializers.ModelSerializer):
    years_subjects = serializers.SerializerMethodField()
    # subjects = serializers.SerializerMethodField()

    def get_years_subjects(self, obj):
        years = Subject.objects.filter(teachers=obj).distinct().values_list("year")
        # years = Year.objects.filter(pk__in=years)
        subjects = []
        for year in years:
            subjects.append(
                {
                    "year": YearSerializer(Year.objects.get(pk=year[0])).data,
                    "subjects": SubjectSerializer(
                        Subject.objects.filter(year=year, teachers=obj), many=True
                    ).data,
                }
            )
        return subjects

    class Meta:
        model = Teacher
        fields = "__all__"


class YearStudentsTeachersSerializer(serializers.ModelSerializer):
    teachers = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()

    def get_teachers(self, obj):
        year = Year.objects.filter(year=obj.year).first()
        subjects = Subject.objects.filter(year=year)
        teachers = subjects.values_list("teachers", flat=True).distinct()
        teachers = [
            TeacherSerializer(Teacher.objects.get(id=teacher)).data
            for teacher in teachers
        ]
        return teachers

    def get_students(self, obj):
        year = Year.objects.filter(year=obj.year).first()
        students = Student.objects.filter(year=year)
        return StudentSerializer(students, many=True).data

    class Meta:
        model = Year
        fields = "__all__"


class YearSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="owner", read_only=True)
    subject_name = serializers.CharField(source="subject", read_only=True)

    class Meta:
        model = Note
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    def get_answers(self, obj):
        answers = Answer.objects.filter(question=obj)
        serializer = AnswerSerializer(answers, many=True)
        return serializer.data

    class Meta:
        model = Question
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    chapter_tag = serializers.IntegerField(source="chapter.number", read_only=True)
    is_over = serializers.SerializerMethodField()

    def get_is_over(self, obj):
        return obj.deadline < timezone.now()

    class Meta:
        model = Quiz
        fields = "__all__"


class FullQuizSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    def get_questions(self, obj):
        questions = Question.objects.filter(quiz=obj)
        return QuestionSerializer(questions, many=True)

    class Meta:
        model = Quiz
        fields = "__all__"


class SubjectBasicTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["teachers"]


class ForumSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source="subject", read_only=True)

    class Meta:
        model = Forum
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author", read_only=True)
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation["attachment"])
        if representation["attachment"] is not None:
            if not representation["attachment"].startswith("http://localhost:8000"):
                representation["attachment"] = (
                    "http://localhost:8000" + representation["attachment"]
                )
        return representation

    class Meta:
        model = Post
        fields = "__all__"


class PostVoteSerializer(serializers.ModelSerializer):

    votes = serializers.SerializerMethodField()

    def get_votes(self, obj):
        votes = obj.get_votes
        return votes

    class Meta:
        model = Post
        fields = ["id", "title", "upvotes", "downvotes", "votes"]


class CommentVoteSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()

    def get_votes(self, obj):
        votes = obj.get_votes
        return votes

    class Meta:
        model = Comment
        fields = ["id", "upvotes", "downvotes", "votes"]


class ForumPostsSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject", read_only=True)
    posts = serializers.SerializerMethodField()

    def get_posts(self, obj):
        posts = Post.objects.filter(forum=obj).all().order_by("date")
        return PostSerializer(posts, many=True).data

    class Meta:
        model = Forum
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    commenter_role = serializers.SerializerMethodField()
    commenter_name = serializers.CharField(source="author", read_only=True)
    votes = serializers.SerializerMethodField()

    def get_votes(self, obj):
        return obj.get_votes

    # og_post_title = serializers.CharField(source='post.title', read_only=True)
    # votes = serializers.SerializerMethodField()

    def get_commenter_role(self, obj):
        commenter = obj.author
        if commenter.is_student:
            return "student"
        if commenter.is_teacher:
            return "teacher"
        return "admin"

    # def get_votes(self, obj):
    #     return obj.get_votes

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation["attachment"])
        if representation["attachment"] is not None:
            if not representation["attachment"].startswith("http://localhost:8000"):
                representation["attachment"] = (
                    "http://localhost:8000" + representation["attachment"]
                )
        return representation

    class Meta:
        model = Comment
        fields = "__all__"


class PostCommentsSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author", read_only=True)
    comments = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    votes = serializers.SerializerMethodField()

    def get_votes(self, obj):
        return obj.get_votes

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj).order_by("-author__is_teacher")
        return CommentSerializer(comments, many=True).data

    class Meta:
        model = Post
        fields = "__all__"


class OtherSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source="chapter.subject", read_only=True)

    class Meta:
        model = Other
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    # attachment = serializers.FileField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation["attachment"])
        if representation["attachment"] is not None:
            if not representation["attachment"].startswith("http://localhost:8000"):
                representation["attachment"] = (
                    "http://localhost:8000" + representation["attachment"]
                )
        if representation["image"] is not None:
            if not representation["image"].startswith("http://localhost:8000"):
                representation["image"] = (
                    "http://localhost:8000" + representation["image"]
                )
        return representation

    class Meta:
        model = News
        fields = "__all__"
