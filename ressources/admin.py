from django.contrib import admin
from .models import Course, Subject, Chapter, TD, TP, Homework, Note, Quiz, Question, Answer, Forum, Post, Comment
# Register your models here.

admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(TD)
admin.site.register(TP)
admin.site.register(Homework)
admin.site.register(Note)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Forum)
admin.site.register(Post)
admin.site.register(Comment)