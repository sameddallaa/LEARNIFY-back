from typing import Any, Iterable, Sequence
from django.dispatch import receiver
from django.db import models
from rest_framework.validators import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, UserManager as BaseUserManager
from django.core.validators import RegexValidator
from .utils import send_password_after_signup, generate_password
import uuid
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, is_student=False, is_staff=True,
                    is_teacher=False, is_superuser=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not (is_student ^ is_teacher ^ is_staff):
            raise ValueError('You must select one role')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_student=is_student,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_teacher=is_teacher,
            # is_editor_teacher=is_editor_teacher,
        )
        if password is None:
            password = generate_password(12)
            
        user.set_password(password)
        send_password_after_signup(password, user)
        user.save(using=self._db)
        return user

    def create_student(self, email, username, first_name, last_name, group, year, password=None, is_student=True, is_staff=False,
                         is_teacher=False, is_superuser=False):
        if not is_student:
            raise ValueError('You must be a student')
        if is_staff or is_teacher or is_superuser:
            raise ValidationError("Wrong flags for student user")
        user = self.create_user(email, username, first_name, last_name, password, is_student, is_staff, is_teacher, is_superuser)
        return user
    
    def bulk_create(self, objs: Iterable, *args, **kwargs):
        for obj in objs:
            obj.save()
        return super().bulk_create(objs, *args, **kwargs)
    def create_superuser(self, email, username, first_name, last_name, password=None, is_student=False, is_staff=True,
                         is_teacher=False, is_superuser=True):
        if not (is_staff and is_superuser):
            raise ValueError('Superusers must have is_staff=True and is_superuser=True')
        user = self.create_user(email, username, first_name, last_name, password, is_student, is_staff, is_teacher, is_superuser)
        return user


class User(AbstractUser, PermissionsMixin):
    
    
    valid_username = RegexValidator(r'^[\w.@+-]+$', 'Enter a valid username')
    valid_name = RegexValidator(r'^[a-zA-Z]+$', 'Enter a valid name')
    
    
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True, null=False, validators=[valid_username])
    first_name = models.CharField(max_length=255, validators=[valid_name])
    last_name = models.CharField(max_length=255, validators=[valid_name])
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not (self.is_student ^ self.is_staff ^ self.is_teacher):
            raise ValidationError('You must choose a role')
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
    
def is_valid_year(year):
    if year < 0 or year > 5:
        raise ValidationError("Year must be 1, 2, 3, 4, or 5.")
    
def is_valid_group(group):
    if group < 0 or group > 10:
        raise ValidationError("Group must be 1, 2, 3, 4, 5, 6, 7, 8, 9, or 10.")


class Year(models.Model):
    year = models.IntegerField(unique=True, default=0, validators=[is_valid_year])
    
    
    class Meta:
        ordering = ['year',]
    def __str__(self):
        return f"Year {str(self.year)}"
    
    
class Group(models.Model):
    year = models.ForeignKey(Year, related_name='groups', null=True, default=0, on_delete=models.SET_NULL)
    number = models.IntegerField(validators=[is_valid_group], default=0)

    class Meta:
        ordering = ['year', 'number']
    def __str__(self):
        return f"{str(self.year)} - Group {str(self.number)}"

class Student(models.Model):   
     
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, default=0,null=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, default=0,null=True, on_delete=models.CASCADE)
    
    
    def save(self, *args, **kwargs):
        year = kwargs.pop('year',0)
        group = kwargs.pop('group',0)
        year, _ = Year.objects.get_or_create(year=year)
        self.year = year
        group, _ = Group.objects.get_or_create(number=group, year=self.year)
        self.group = group
            
        if self.group.year != self.year:
            raise ValidationError("Group and year do not match.")
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.user)


class Teacher(models.Model):
    
    
    CHOICES = (
        ('PROFESSEUR', 'Professeur'),
        ('MAITRE ASSISTANT A', 'Maître assistant A'),
        ('MAITRE ASSISTANT B', 'Maître assistant B'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=255, null=True) 
    
    
    def save(self, *args, **kwargs):
        degree = kwargs.pop('degree', "")
        # self.degree = degree
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return str(self.user)

class UploadedFile(models.Model):
    file = models.FileField()
    uploaded_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.uploaded_on.date()