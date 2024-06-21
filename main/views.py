from django.conf import settings
from django.shortcuts import render, redirect

def index(request):
    if not request.user.is_anonymous:
        return redirect('user/dashboard')
    else:
        return render(request, 'index.html')

def userLogin(request):
    if not request.user.is_anonymous:
        return redirect('user/dashboard')
    else:
        return render(request, 'login.html')

def userSignup(request):
    if not request.user.is_anonymous:
        return redirect('user/dashboard')
    else:
        return render(request, 'signup.html')