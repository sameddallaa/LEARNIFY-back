from django.db import models
from profiles.models import User, Teacher, Year
# Create your models here.


def valid_coeff(coeff):
    if coeff < 0:
        raise ValueError('Coefficient must be a positive number')

class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    main_teacher = models.ForeignKey(Teacher, null=True, on_delete=models.SET_NULL)
    teachers = models.ManyToManyField(Teacher, related_name='subjects',)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    coefficient = models.IntegerField(validators=[valid_coeff])
    credit = models.IntegerField()
    
    
    def save(self, *args, **kwargs):
        print(self.teachers)
        # if self.main_teacher not in self.teachers:
        #     self.teachers.add(self.main_teacher)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    # teacher = 
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)
    content = models.FileField(upload_to='courses/')
    
    def __str__(self):
        return self.title