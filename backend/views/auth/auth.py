from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.models import User
from backend.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from backend.forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseBadRequest, JsonResponse

@api_view(['GET', 'POST'])
def backendsignup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Process valid form data
            profile_name = form.cleaned_data['profile_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Create and save user
            user = User.objects.create(username=username, profile_name=profile_name)
            user.set_password(password)
            user.save()

            # Add success message
            messages.success(request, 'User registered successfully. Please Log in.')

            # Redirect to login page
            return redirect('login')
    else:
        # If request method is GET, initialize an empty form
        form = SignupForm(initial=request.POST)

    # Render initial form
    return render(request, 'signup.html', {'form': form})

def backendlogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Fetch user based on username (email)
            user = User.objects.filter(username=username).first()
            if user:
                # Check if account is locked
                if user.lockout_timestamp and user.lockout_timestamp > timezone.now():
                    remaining_seconds = (user.lockout_timestamp - timezone.now()).total_seconds()
                    minutes = int(remaining_seconds // 60)
                    seconds = int(remaining_seconds % 60)
                    request.session['sweet_alert'] = {
                        'title': 'Account Locked',
                        'text': f'Account locked due to multiple failed attempts. Please try again in {minutes} minutes and {seconds} seconds.',
                        'icon': 'error'
                    }
                    return redirect('login')  # Redirect to login page
                # Attempt to authenticate user
                authenticated_user = authenticate(request, username=username, password=password)
                if authenticated_user is not None:
                    # Reset failed login attempts on successful login
                    user.failed_login_attempts = 0
                    user.save()
                    login(request, authenticated_user)
                    # Redirect to a success page
                    return redirect('user/dashboard')
                else:
                    # Increment failed login attempts
                    user.failed_login_attempts += 1
                    user.save()
                    
                    # Check if user has exceeded maximum failed login attempts
                    attempts_remaining = 3 - user.failed_login_attempts
                    if user.failed_login_attempts >= 3:
                        # Lock the account for 5 minutes
                        user.lockout_timestamp = timezone.now() + timezone.timedelta(minutes=5)
                        user.failed_login_attempts = 0  # Reset failed login attempts
                        user.save()
                        remaining_seconds = (user.lockout_timestamp - timezone.now()).total_seconds()
                        minutes = int(remaining_seconds // 60)
                        seconds = int(remaining_seconds % 60)
                        request.session['sweet_alert'] = {
                            'title': 'Account Locked',
                            'text': f'Account locked due to multiple failed attempts. Please try again in {minutes} minutes and {seconds} seconds.',
                            'icon': 'error'
                        }
                    else:
                        request.session['sweet_alert'] = {
                            'title': 'Oops',
                            'text': f'Incorrect Password. Please try again. Attempts remaining: {attempts_remaining}',
                            'icon': 'error'
                        }
                    return redirect('login')  # Redirect to login page
            else:
                request.session['sweet_alert'] = {
                    'title': 'Not Found',
                    'text': 'User does not exist. Please check your credentials.',
                    'icon': 'error'
                }
                return redirect('login')  # Redirect to login page
        else:
            # Form is not valid, return bad request response
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = LoginForm()

    # Render the login form in case of GET request
    return render(request, 'login.html', {'form': form})

@api_view(['GET'])
def backendlogout(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            logout(request)
            return redirect('login')
        else:
            return redirect(request.get_full_path())