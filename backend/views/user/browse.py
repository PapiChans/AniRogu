import requests
from django.shortcuts import render, redirect
from backend.forms import SearchAnimeForm
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view

def backendSearchAnime(request):
    if request.method == 'POST':
        form = SearchAnimeForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['animekeyword']
            page = 1
            return redirect(f'/user/browse/q={keyword}/page={page}')
        else:
            form = SearchAnimeForm()
            if request.user.is_anonymous:
                return redirect('index')
            else:
                return redirect('user/home')
