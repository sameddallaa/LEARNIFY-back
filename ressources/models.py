from django.db import models
from profiles.models import User, Teacher, Year
# Create your models here.


def valid_coeff(coeff):
    if coeff < 0:
        raise ValueError('Coefficient must be a positive number')

class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.SET_NULL)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    coefficient = models.IntegerField(validators=[valid_coeff])
    
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)
    content = models.FileField(upload_to='courses/')
    
    def __str__(self):
        return self.title