from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/signup', views.backendsignup, name="auth/signup"),
    path('auth/login', views.backendlogin, name="auth/login"),
    path('auth/logout', views.backendlogout, name="auth/logout"),
]