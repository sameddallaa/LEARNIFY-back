from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from .users import User
# Create your models here.

class Student(models.Model):    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)
    def __str__(self):
        return str(self.user)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=255, null=True) # add choices for degree
    
    def __str__(self):
        return str(self.user)
    