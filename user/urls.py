from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Homepage
    path('home', views.userHome, name='user/home'),
    path('browse/q=<str:keyword>', views.userAnimeBrowse, name='user/browse'),
]