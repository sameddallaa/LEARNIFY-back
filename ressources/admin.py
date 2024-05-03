from django.contrib import admin
from .models import Course, Subject, Chapter, TD
# Register your models here.

admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(TD)