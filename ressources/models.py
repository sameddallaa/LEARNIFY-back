from django.db import models
from profiles.models import User
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    teacher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    coefficient = models.IntegerField()
    
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    content = models.TextField()
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.title