from django.urls import path
from rest_framework import permissions
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # path('', view=views.ProfileView, name='Profiles')
    # path('students/', view=views.StudentView.as_view(), name='Students')
    path('auth/signup/', view=views.SignupView.as_view(), name='SignupView'),
    path('auth/login/', view=views.LoginView.as_view(), name='LoginView'),
    path('jwt/create/', view=TokenObtainPairView.as_view(), name='JWTCreateView'),
    path('jwt/refresh/', view=TokenRefreshView.as_view(), name='JWTRefreshView'),
    path('jwt/verify/', view=TokenVerifyView.as_view(), name='JWTVerifyView'),
]
