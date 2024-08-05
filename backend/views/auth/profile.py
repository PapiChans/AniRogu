from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.models import User
from backend.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from backend.forms import ChangeProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseBadRequest, JsonResponse

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