from rest_framework.validators import ValidationError
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Student, Teacher, UploadedFile, User, Year, Group


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    username = serializers.CharField(
        max_length=511, default=str(first_name) + str(last_name)
    )
    password = serializers.CharField(min_length=8, write_only=True)
    is_student = serializers.BooleanField(default=True)
    is_teacher = serializers.BooleanField(default=False)
    is_staff = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_student",
            "is_teacher",
            "is_staff",
        ]

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get("email")).exists():
            raise ValidationError("Email already exists")
        if User.objects.filter(username=attrs.get("username")).exists():
            raise ValidationError("Username already exists")
        has_multiple_roles = not (
            attrs.get("is_student") ^ attrs.get("is_teacher") ^ attrs.get("is_staff")
        )
        if has_multiple_roles:
            raise ValidationError("You must select only one role")
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data["password"]
        user = super().create(validated_data)
        user.set_password(password)
        is_teacher = validated_data["is_teacher"]
        # if is_editor_teacher and not is_teacher:
        #     validated_data['is_teacher'] = True
        user.save()
        Token.objects.create(user=user)
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name

        if user.is_student:
            try:
                student = Student.objects.get(user=user)
                token["is_student"] = True
                token["student_id"] = student.id
                token["year"] = str(student.year.year)
                token["year_tag"] = str(student.year)
                token["group"] = str(student.group.number)
            except Student.DoesNotExist:
                raise ValidationError("Student model instance does not exist")
        elif user.is_teacher:
            try:
                teacher = Teacher.objects.get(user=user)
                token["is_teacher"] = True
                token["teacher_id"] = teacher.id
                token["degree"] = teacher.degree
                # token['is_editor'] = 'Yes' if user.is_editor_teacher else 'No'
            except Teacher.DoesNotExist:
                raise ValidationError("Teacher model instance does not exist")
        return token


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = "__all__"


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangeNameSerializer(serializers.Serializer):
    model = User

    first_name = serializers.CharField()
    last_name = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user", read_only=True)
    group_tag = serializers.CharField(source="group.number", read_only=True)
    year_tag = serializers.CharField(source="year.year", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Student
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source="user", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Teacher
        fields = "__all__"


class YearSerializer(serializers.ModelSerializer):
    year_tag = serializers.CharField(source="__str__", read_only=True)

    class Meta:
        model = Year
        fields = "__all__"


class TeacherYearsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = [
            "year",
        ]


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ["number", "year"]
