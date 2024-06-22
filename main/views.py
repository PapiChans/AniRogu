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
    
def userForgot(request):
    if not request.user.is_anonymous:
        return redirect('user/dashboard')
    else:
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            message = "Temporary service not available."
            return render(request, 'login.html', {
                'forgot': True,
                'message': message
            })
        else:
            return render(request, 'forgot-password.html')