from django.urls import path
from .models import Course
from . import views

urlpatterns = [
    path('subjects/', view=views.SubjectsListView.as_view(), name='SubjectsListView'),
    path('subjects/<int:id>', view=views.SubjectsRetriveView.as_view(), name='SubjectsRetrieveView'),
    path('subjects/create/', view=views.SubjectsCreateView.as_view(), name='SubjectsCreateView'),
    path('subjects/<int:id>/delete/', view=views.SubjectsDeleteView.as_view(), name='SubjectsDeleteView'),
    path('subjects/<int:id>/update/', view=views.SubjectsUpdateView.as_view(), name='SubjectsUpdateView'),
    path('courses/', view=views.CoursesListView.as_view(), name='CoursesListView'),
    path('courses/<int:id>', view=views.CoursesRetriveView.as_view(), name='CoursesRetrieveView'),
    path('courses/create/', view=views.CoursesCreateView.as_view(), name='CoursesCreateView'),
    path('courses/<int:id>/delete/', view=views.CoursesDeleteView.as_view(), name='CoursesDeleteView'),
    path('courses/<int:id>/update/', view=views.CoursesUpdateView.as_view(), name='CoursesUpdateView'),
]
