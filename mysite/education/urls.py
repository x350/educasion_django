from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from .views import register, user_login, user_logout, index, CoursesListView, CourseDetailView, LessonDetailView, \
    StudentsListView, StudentDetailView


app_name = 'education'

urlpatterns = [
    path("", index, name='index'),
    path("courses/", CoursesListView.as_view(), name="courses_list"),
    path("course/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("lesson/<int:pk>/", LessonDetailView.as_view(), name="lesson_detail"),
    path("students/", StudentsListView.as_view(), name="students_list"),
    path("student/<int:pk>/", StudentDetailView.as_view(), name='student_detail'),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    re_path(r'^_nested_admin/', include('nested_admin.urls')),
    ]

