from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Student, Teacher, User, Year, Group


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            student = Student.objects.create(user=instance)
            student.year, _ = Year.objects.get_or_create(year=0)
            print('it works so far')
            student.group, _ = Group.objects.get_or_create(number=0, year=student.year)
            # year = kwargs.get('year')
            # group = kwargs.get('group')
            # if year:
            #     y, _ = Year.objects.get_or_create(year=year)
            #     student.year = y
            # if group:
            #     g, _ = Group.objects.get_or_create(number=group, year=y)
            #     student.group = g
            student.save()
        elif instance.is_teacher:
            teacher = Teacher.objects.create(user=instance)
            teacher.save()

# @receiver(post_save, sender=Student)
# def add_group_and_year(sender, instance, created, **kwargs):
#     if created:
        

@receiver(post_delete, sender=Student)
def delete_profile(sender, instance, **kwargs):
    user = instance.user
    user.delete()


@receiver(post_delete, sender=Teacher)
def delete_profile(sender, instance, **kwargs):
    user = instance.user
    user.delete()
