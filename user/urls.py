from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Homepage
    path('dashboard', views.userDashboard, name='user/dashboard'),
]