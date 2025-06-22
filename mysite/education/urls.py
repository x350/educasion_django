from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from .views import register, user_login, user_logout, index


app_name = 'education'

urlpatterns = [
    path("", index, name='index'),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    ]
