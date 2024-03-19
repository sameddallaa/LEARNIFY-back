from django.urls import path
from . import views

urlpatterns = [
    # path('', view=views.ProfileView, name='Profiles')
    # path('students/', view=views.StudentView.as_view(), name='Students')
    path('auth/signup', view=views.SignupView.as_view(), name='SignupView'),
    path('auth/login', view=views.LoginView.as_view(), name='LoginView'),
]
