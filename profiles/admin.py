from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from .models import User
from .forms import UserCreationForm
# Register your models here.

class UserAdmin(BaseAdmin):
    
    add_form = UserCreationForm
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
    
admin.site.register(User, UserAdmin)
