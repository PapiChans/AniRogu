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
        forgot = request.session.pop('forgot', False) # For Forgot Password Page
        message = request.session.pop('message', '') # For Forgot Password Page
        sweet_alert = request.session.pop('sweet_alert', None) # For Login Errors

        # Your login view logic here

        return render(request, 'login.html', {
            'forgot': forgot,
            'message': message,
            'sweet_alert': sweet_alert,
        })

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
            request.session['forgot'] = True
            request.session['message'] = message
            # Redirect to login page with query parameters
            return redirect('login')  # Replace 'login' with your actual login URL
        else:
            # Redirect to forgot password page
            return redirect('forgot_password')