from django.contrib import admin
from .models import Course, Subject, Chapter
# Register your models here.

admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Chapter)