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

    # Browse HAnime
    path('backend/SearchHAnime', views.backendSearchHAnime, name="backend/SearchHAnime"),

    # Profile
    path('backend/ChangeProfile', views.backendChangeProfile, name='backend/ChangeProfile'),
    path('backend/ChangePassword', views.backendChangePassword, name='backend/ChangePassword'),

    # Anime List
    path('backend/AddAnime/', views.backendAddAnime, name='backend/AddAnime'),
    path('backend/RemoveAnime/', views.backendRemoveAnime, name='backend/RemoveAnime'),

    # Anime Episode
    path('backend/RemoveAnime2/<uuid:anime_Id>', views.backendRemoveAnime2, name='backend/RemoveAnime2'),
    path('backend/WatchingEpisode/<uuid:episode_Id>', views.backendWatchingEpisode, name='backend/WatchingEpisode'),
    path('backend/CompletedEpisode/<uuid:episode_Id>', views.backendCompletedEpisode, name='backend/CompletedEpisode'),
    path('backend/AnimeMarkAsCompleted/<uuid:anime_Id>', views.backendAnimeMarkAsCompleted, name='backend/AnimeMarkAsCompleted'),
]