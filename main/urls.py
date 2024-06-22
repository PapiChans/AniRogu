from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),

    path('login', views.userLogin, name='login'),
    path('signup', views.userSignup, name='signup'),
    path('forgot-password', views.userForgot, name='forgot-password'),
]