from django.urls import path
from .models import Course
from . import views

urlpatterns = [
    path('ressources/subjects', view=views.SubjectsListView.as_view(), name='SubjectsListView'),
    path('ressources/subjects/year/<int:year>', view=views.SubjectYearView.as_view(), name='SubjectsListView'),
    path('ressources/subjects/<int:id>', view=views.SubjectsRetriveView.as_view(), name='SubjectsRetrieveView'),
    path('ressources/subjects/create/', view=views.SubjectsCreateView.as_view(), name='SubjectsCreateView'),
    # path('ressources/subjects/<int:id>/delete/', view=views.SubjectsDeleteView.as_view(), name='SubjectsDeleteView'),
    path('ressources/subjects/<int:id>/update/', view=views.SubjectsUpdateView.as_view(), name='SubjectsUpdateView'),
    path('ressources/<int:id>/chapters/', view=views.ChapterView.as_view(), name='ChapterView'),
    path('ressources/courses/', view=views.CoursesListView.as_view(), name='CoursesListView'),
    path('ressources/course/<int:id>', view=views.CourseRetrieveView.as_view(), name='CourseRetrieveView'),
    path('ressources/courses/<int:id>', view=views.CoursesRetriveView.as_view(), name='CoursesRetrieveView'),
    path('ressources/td/<int:subject>/<int:chapter>/', view=views.TDRetrieveView.as_view(), name='TDRetrieveView'),
    path('ressources/courses/create/', view=views.CoursesCreateView.as_view(), name='CoursesCreateView'),
    path('ressources/courses/<int:id>/delete/', view=views.CoursesDeleteView.as_view(), name='CoursesDeleteView'),
    path('ressources/courses/<int:id>/update/', view=views.CoursesUpdateView.as_view(), name='CoursesUpdateView'),
    path('teachers/<int:teacher>/subjects/', view=views.TeacherSubjectsView.as_view(), name='TeacherSubjectsView'),
    path('teachers/<int:teacher>/<int:year>/subjects/', view=views.TeacherSubjectPerYearView.as_view(), name='TeacherSubjectPerYearView'),
]
