from django.urls import path
from rest_framework import permissions
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # path('', view=views.ProfileView, name='Profiles')
    # path('students/', view=views.StudentView.as_view(), name='Students')
    path('users/', view=views.UserListView.as_view(), name='UserListView'),
    path('users/<int:pk>/change-password/', view=views.ChangePasswordView.as_view(), name='ChangePasswordView'),
    path('students/', view=views.StudentListView.as_view(), name='StudentListView'),
    path('teachers/', view=views.TeacherListView.as_view(), name='TeacherListView'),
    path('auth/signup/', view=views.SignupView.as_view(), name='SignupView'),
    path('csv-signup/', view=views.FileUploadAPIView.as_view(), name='csv_bulk_signup'),
    path('auth/login/', view=views.LoginView.as_view(), name='LoginView'),
    path('jwt/create/', view=TokenObtainPairView.as_view(), name='JWTCreateView'),
    path('jwt/refresh/', view=TokenRefreshView.as_view(), name='JWTRefreshView'),
    path('jwt/verify/', view=TokenVerifyView.as_view(), name='JWTVerifyView'),
]
