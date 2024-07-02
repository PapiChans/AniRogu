import requests
from django.shortcuts import render, redirect
from backend.forms import SearchAnimeForm
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view

def backendSearchAnime(request):
    if request.user.is_anonymous:
        message = "Action not Available, Login First."
        request.session['error'] = True
        request.session['message'] = message
        # Redirect to login page with query parameters
        return redirect('login')  # Replace 'login' with your actual login URL
    else:
        if request.method == 'POST':
            form = SearchAnimeForm(request.POST)
            if form.is_valid():
                keyword = form.cleaned_data['animekeyword']
                return redirect(f'/user/browse/q={keyword}')
            else:
                form = SearchAnimeForm()

    return redirect('user/home')
