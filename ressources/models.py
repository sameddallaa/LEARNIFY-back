from django.db import models
from profiles.models import User, Teacher, Year
# Create your models here.


def valid_coeff(coeff):
    if coeff < 0:
        raise ValueError('Coefficient must be a positive number')

class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    main_teacher = models.ForeignKey(Teacher, null=True, on_delete=models.SET_NULL)
    teachers = models.ManyToManyField(Teacher, related_name='subjects',default=[main_teacher], null=True, blank=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    coefficient = models.IntegerField(validators=[valid_coeff])
    credit = models.IntegerField()
    place = models.CharField(default='Amphi D', max_length=255)
    
    
    def save(self, *args, **kwargs):
        # if self.main_teacher not in self.teachers:
        #     self.teachers.add(self.main_teacher)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    
    
class Chapter(models.Model):
    
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    number = models.IntegerField(default=1)
    
    
    def save(self, *args, **kwargs):
        existing_chapters = Chapter.objects.filter(subject=self.subject).count()
        self.number = existing_chapters + 1
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    chapter = models.ForeignKey(Chapter, null=True, on_delete=models.SET_NULL)
    content = models.FileField(upload_to='courses/')
    
    def __str__(self):
        return self.title
    
class TD(models.Model):
    
    class Meta:
        verbose_name = 'TD'
        verbose_name_plural = 'TDs'
        
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    chapter = models.ForeignKey(Chapter, null=True, on_delete=models.SET_NULL)
    content = models.FileField(upload_to='tds/')
    
    def __str__(self):
        return self.title
    
    
class TP(models.Model):
    
    class Meta:
        verbose_name = 'TP'
        verbose_name_plural = 'TPs'
        
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    chapter = models.ForeignKey(Chapter, null=True, on_delete=models.SET_NULL)
    content = models.FileField(upload_to='tps/')
    
    def __str__(self):
        return self.title