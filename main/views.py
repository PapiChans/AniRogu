from django.conf import settings
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')