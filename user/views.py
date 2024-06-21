from django.conf import settings
from django.shortcuts import render, redirect

# Create your views here.
def userDashboard(request):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        return render(request, 'dashboard.html')