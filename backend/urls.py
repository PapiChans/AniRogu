from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Authentication
    path('auth/signup', views.backendsignup, name="auth/signup"),
    path('auth/login', views.backendlogin, name="auth/login"),
    path('auth/logout', views.backendlogout, name="auth/logout"),
    path('auth/forgot', views.backendaccountrecovery, name="auth/forgot"),

    # Browse Anime
    path('backend/SearchAnime', views.backendSearchAnime, name="backend/SearchAnime"),

    # Profile
    path('backend/ChangeProfile', views.backendChangeProfile, name='backend/ChangeProfile'),
    path('backend/ChangePassword', views.backendChangePassword, name='backend/ChangePassword'),

    # Anime List
    path('backend/AddAnime/', views.backendAddAnime, name='backend/AddAnime'),
    path('backend/RemoveAnime/', views.backendRemoveAnime, name='backend/RemoveAnime'),
]