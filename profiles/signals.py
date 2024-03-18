from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .users import User
from .models import Student, Teacher
#
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.is_student:
        print("signal sent")
        student = Student.objects.create(user=instance)
        student.save()
    elif created and instance.is_teacher:
        teacher = Teacher.objects.create(user=instance)
        teacher.save()
        
@receiver(post_delete, sender=Student)
def delete_profile(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    
@receiver(post_delete, sender=Teacher)
def delete_profile(sender, instance, **kwargs):
    user = instance.user
    user.delete()