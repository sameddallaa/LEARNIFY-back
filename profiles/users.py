# from django.db import models
# from rest_framework.validators import ValidationError
# from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, UserManager as BaseUserManager
# from django.core.validators import RegexValidator
# from .models import Student

# # Create your models here.

# class UserManager(BaseUserManager):
#     def create_user(self, email, username, first_name, last_name, password=None, is_student=False, is_staff=True,
#                     is_teacher=False, is_editor_teacher=False, is_superuser=False):
#         if not email:
#             raise ValueError('Users must have an email address')
#         if not username:
#             raise ValueError('Users must have a username')
#         if not first_name:
#             raise ValueError('Users must have a first name')
#         if not last_name:
#             raise ValueError('Users must have a last name')
#         if not (is_student ^ is_teacher ^ is_staff):
#             raise ValueError('You must select one role')
#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             is_student=is_student,
#             is_staff=is_staff,
#             is_superuser=is_superuser,
#             is_teacher=is_teacher,
#             is_editor_teacher=is_editor_teacher,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_student(self, email, username, first_name, last_name, major, year, password=None, is_student=True, is_staff=False,
#                          is_teacher=False, is_editor_teacher=False, is_superuser=False):
#         if not is_student:
#             raise ValueError('You must be a student')
#         if is_staff or is_teacher or is_editor_teacher or is_superuser:
#             raise ValidationError("Wrong flags for student user")
#         user = self.create_user(email, username, first_name, last_name, password, is_student, is_staff, is_teacher, is_editor_teacher, is_superuser)
#         student = Student.objects.get(user = user)
#         student.major = major
#         student.year = year
        
#         student.save()
#         return user
        
#     def create_superuser(self, email, username, first_name, last_name, password=None, is_student=False, is_staff=True,
#                          is_teacher=False, is_editor_teacher=False, is_superuser=True):
#         if not (is_staff and is_superuser):
#             raise ValueError('Superusers must have is_staff=True and is_superuser=True')
#         user = self.create_user(email, username, first_name, last_name, password, is_student, is_staff, is_teacher,
#                                 is_editor_teacher, is_superuser)
#         return user


# class User(AbstractUser, PermissionsMixin):
#     valid_username = RegexValidator(r'^[\w.@+-]+$', 'Enter a valid username')
#     valid_name = RegexValidator(r'^[a-zA-Z]+$', 'Enter a valid name')
#     email = models.EmailField(max_length=255, unique=True)
#     username = models.CharField(max_length=255, unique=True, null=False, validators=[valid_username])
#     first_name = models.CharField(max_length=255, validators=[valid_name])
#     last_name = models.CharField(max_length=255, validators=[valid_name])
#     # password = models.CharField(max_length=255)
#     is_staff = models.BooleanField(default=False)
#     is_teacher = models.BooleanField(default=False)
#     is_editor_teacher = models.BooleanField(default=False)
#     is_student = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

#     objects = UserManager()

#     def save(self, *args, **kwargs):
#         if not (self.is_student ^ self.is_staff ^ self.is_teacher):
#             raise ValidationError('You must choose a role')
#         if self.is_editor_teacher and not self.is_teacher:
#             self.is_teacher = True
#         self.set_password(self.password)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
