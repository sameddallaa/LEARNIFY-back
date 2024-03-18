from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, UserManager as BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None ,is_student=False, is_staff=False, is_teacher=False, is_editor_teacher=False, is_superuser=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_student=is_student,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_teacher=is_teacher,
            is_editor_teacher=is_editor_teacher,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_studentuser(self, email, username, first_name, last_name, password=None, is_student=True, is_staff=False, is_teacher=False, is_editor_teacher=False, is_superuser=False):
        if not is_student:
            raise ValueError('Staff users must have is_staff=True')
        user = self.create_user(email, username, first_name, last_name, password, is_student, is_staff, is_teacher, is_editor_teacher, is_superuser)
        return user
    
    def create_staffuser(self, email, username, first_name, last_name, password=None, is_student=False, is_staff=True, is_teacher=False, is_editor_teacher=False, is_superuser=False):
        if not is_staff:
            raise ValueError('Staff users must have is_staff=True')
        user = self.create_user(email, username, first_name, last_name, password, is_student, is_staff, is_teacher, is_editor_teacher, is_superuser)
        return user
    
    def create_teacheruser(self, email, username, first_name, last_name, password=None, is_student=False, is_staff=False, is_teacher=True, is_editor_teacher=False, is_superuser=False):
        if not is_teacher:
            raise ValueError('Teachers must have is_teacher=True')
        user = self.create_user(email, username, first_name, last_name, password, is_student, is_staff, is_teacher, is_editor_teacher, is_superuser)
        return user
    
    def create_superuser(self, email, username, first_name, last_name ,password=None, is_student=False, is_staff=True, is_teacher=False, is_editor_teacher=False, is_superuser=True):
        if not (is_staff and is_superuser):
            raise ValueError('Superusers must have is_staff=True and is_superuser=True')
        user = self.create_user(email, username, first_name, last_name, password, is_student, is_staff, is_teacher, is_editor_teacher, is_superuser)        
        return user
    
    

class User(AbstractUser, PermissionsMixin):       
    
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True, null=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_editor_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"