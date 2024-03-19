from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from .users import User
from .models import Teacher, Student
# Register your models here.

class UserAdmin(BaseAdmin):
    list_display = ('username', 
                    'email',
                    'first_name',
                    'last_name',
                    'is_staff',
                    'is_student',
                    'is_teacher',
                    'is_editor_teacher', 
                    'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_student', 'is_teacher', 'is_editor_teacher', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
    (
        None,
        {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "username", "password1", "password2", 'is_staff', 'is_student', 'is_teacher', 'is_editor_teacher', 'is_superuser'),
        },
    ),
)

    
admin.site.register(User, UserAdmin)
admin.site.register(Teacher)
admin.site.register(Student)