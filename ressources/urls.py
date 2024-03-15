from django.urls import path
from .models import Course
from . import views

urlpatterns = [
    path('subjects/', view=views.SubjectsListView.as_view(), name='SubjectsListView'),
    path('subjects/<int:id>', view=views.SubjectsRetriveView.as_view(), name='SubjectsRetrieveView'),
    path('subjects/create/', view=views.SubjectsCreateView.as_view(), name='SubjectsCreateView'),
    path('subjects/delete/<int:id>', view=views.SubjectsDeleteView.as_view(), name='SubjectsDeleteView'),
    path('subjects/update/<int:id>', view=views.SubjectsUpdateView.as_view(), name='SubjectsUpdateView'),
    path('courses/', view=views.CoursesListView.as_view(), name='CoursesListView'),
    path('courses/<int:id>', view=views.CoursesRetriveView.as_view(), name='CoursesRetrieveView'),
    path('courses/create/', view=views.CoursesCreateView.as_view(), name='CoursesCreateView'),
    path('courses/delete/<int:id>', view=views.CoursesDeleteView.as_view(), name='CoursesDeleteView'),
    path('courses/update/<int:id>', view=views.CoursesUpdateView.as_view(), name='CoursesUpdateView'),
]
