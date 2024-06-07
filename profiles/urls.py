from django.urls import path
from rest_framework import permissions
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("users/", view=views.UserListView.as_view(), name="UserListView"),
    path(
        "users/<int:pk>/change-password/",
        view=views.ChangePasswordView.as_view(),
        name="ChangePasswordView",
    ),
    path("students/", view=views.StudentListView.as_view(), name="StudentListView"),
    path("teachers/", view=views.TeacherListView.as_view(), name="TeacherListView"),
    path(
        "teachers/<int:teacher>/years/",
        view=views.TeachersYearsView.as_view(),
        name="TeacherYearsView",
    ),
    path("auth/signup/", view=views.SignupView.as_view(), name="SignupView"),
    path(
        "users/<int:pk>/delete",
        view=views.UserDeleteView.as_view(),
        name="UserDeleteView",
    ),
    path(
        "teachers/<int:pk>",
        view=views.TeacherRetrieveView.as_view(),
        name="TeacherRetrieveView",
    ),
    path(
        "csv-signup/students",
        view=views.FileUploadStudentsAPIView.as_view(),
        name="csv_bulk_signup",
    ),
    path(
        "csv-signup/teachers",
        view=views.FileUploadTeacherAPIView.as_view(),
        name="csv_bulk_signup_teachers",
    ),
    path("auth/login/", view=views.MyTokenObtainPairView.as_view(), name="LoginView"),
    path(
        "change-name/<int:pk>/",
        view=views.ChangeNameView.as_view(),
        name="ChangeNameView",
    ),
    # path('jwt/create/', view=TokenObtainPairView.as_view(), name='JWTCreateView'),
    path("auth/login/refresh/", view=TokenRefreshView.as_view(), name="JWTRefreshView"),
    path("jwt/verify/", view=TokenVerifyView.as_view(), name="JWTVerifyView"),
    path("years/", view=views.YearListView.as_view(), name="YearListView"),
    path("groups/", view=views.GroupListView.as_view(), name="GroupListView"),
]
