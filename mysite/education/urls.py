from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from .views import register, user_login, user_logout, index, CoursesListView, CourseDetailView, LessonDetailView, \
    StudentsListView, StudentDetailView, TeachersListView, TeacherDetailView, CourseCreateView, CourseUpdateView, \
    CourseDeleteView, LessonListView, LessonUpdateView, LessonDeleteView, LessonCreateView

app_name = 'education'

urlpatterns = [

    path("", index, name='index'),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("courses/", CoursesListView.as_view(), name="courses_list"),
    path("courses/create/", CourseCreateView.as_view(), name="course_create"),

    path("students/", StudentsListView.as_view(), name="students_list"),
    path("teachers/", TeachersListView.as_view(), name="teachers_list"),
    path("course/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("course/update/<int:pk>/", CourseUpdateView.as_view(), name="course_update"),
    path("course/delete/<int:pk>/", CourseDeleteView.as_view(), name="course_delete"),

    path("teacher/<int:pk>/", TeacherDetailView.as_view(), name='teacher_detail'),
    path("student/<int:pk>/", StudentDetailView.as_view(), name='student_detail'),

    path("lessons/", LessonListView.as_view(), name="lessons_list"),
    path("lesson/<int:pk>/", LessonDetailView.as_view(), name="lesson_detail"),
    path("lesson/create/<int:pk>/", LessonCreateView.as_view(), name="lesson_create"),
    path("lesson/update/<int:pk>/", LessonUpdateView.as_view(), name="lesson_update"),
    path("lesson/delete/<int:pk>/", LessonDeleteView.as_view(), name="lesson_delete"),

    re_path(r'^_nested_admin/', include('nested_admin.urls')),

    ]

