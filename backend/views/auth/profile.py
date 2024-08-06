from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from backend.forms import ChangeProfileForm, ChangePasswordForm
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

def backendChangeProfile(request):
    if request.method == 'POST':
        form = ChangeProfileForm(request.POST)
        if form.is_valid():
            new_profile_name = form.cleaned_data['new_profile_name']

            user =  User.objects.get(user_Id = request.user.user_Id)         
            user.profile_name = new_profile_name
            user.save()

            context = {
                'message': 'Change Profile Name Successfully',
                'success': True,
                'profile_name': new_profile_name,
            }

            return render(request, 'profile.html', context)
        else:
            context = {
                'message': 'Change Profile Name Failed',
                'error': True,
                'profile_name': user.profile_name,
            }
            return render(request, 'profile.html', context)
    else:
        form = ChangeProfileForm()

    # Render the login form in case of GET request
    return render(request, 'profile.html', {'form': form})

def backendChangePassword(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            password = form.cleaned_data['password']
            cnfm_password = form.cleaned_data['cnfm_password']

            user =  User.objects.get(user_Id = request.user.user_Id)

            hashed_old_password = make_password(old_password)

            if check_password(old_password, user.password):
                if password != cnfm_password:
                    context = {
                    'message': 'New Passwords not match',
                    'error': True,
                    }
                    return render(request, 'profile.html', context)
                else:
                    user.set_password(password)
                    user.save()
                    context = {
                        'message': 'Change Password Successfully',
                        'success': True,
                    }
                    # Add success message
                    messages.success(request, 'Change Password Successfully. Please Log in.')

                    # Redirect to login page
                    return redirect('login')
            else:
                context = {
                'message': 'Incorrect Old Password',
                'error': True,
                }
                return render(request, 'profile.html', context)
        else:
            context = {
                'message': 'Change Password Failed',
                'error': True,
            }
            return render(request, 'profile.html', context)
    else:
        form = ChangePasswordForm()

    # Render the login form in case of GET request
    return render(request, 'profile.html', {'form': form})