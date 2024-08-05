from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Homepage
    path('home', views.userHome, name='user/home'),
    path('browse/q=<str:keyword>/page=<int:page>', views.userAnimeBrowse, name='user/browse'),
    path('browse/genres=<str:genres>/page=<int:page>', views.userAnimeGenre, name='user/browse/genre'),
    path('browse/upcoming/page=<int:page>', views.userAnimeUpcoming, name='user/browse/upcoming'),
    path('anime/id=<str:id>', views.userAnimeInfo, name='user/anime/id'),
    path('about', views.userAbout, name='user/about'),
    path('profile', views.userProfile, name='user/profile')
]