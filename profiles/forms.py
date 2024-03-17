# forms.py
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name' ,)
        # fields = ['username', 'first_name', 'last_name', 'is_student', 'is_teacher', 'is_editor_teacher', 'is_staff', 'is_superuser']
