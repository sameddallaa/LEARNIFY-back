from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Subject, Forum

@receiver(post_save, sender=Subject)
def create_forum(sender, instance, created, **kwargs):
    if created:
        forum = Forum.objects.create(subject=instance)
        forum.save()