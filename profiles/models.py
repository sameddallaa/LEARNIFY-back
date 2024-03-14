from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(post_delete, sender=Profile)
def pre_delete_delete_user(sender, instance, *args, **kwargs):
    if instance.user:
        instance.user.delete()

class Student(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    major = models.CharField(max_length=255, blank=True, null=True) # to change later
    year = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        user = self.profile.user
        return f"{user.first_name} {user.last_name}"
    
class Teacher(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    rank = models.CharField(max_length=255) # add choices later
    
    def __str__(self):
        user = self.profile.user
        return f"{user.first_name} {user.last_name}"