from django.conf import settings
from django.shortcuts import render, redirect
import requests

# Create your views here.
def userHome(request):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        # Make a request to the external API
        api_url = f'https://api.jikan.moe/v4/seasons/upcoming'
        response = requests.get(api_url)
        
        if response.status_code == 200:
            # Assuming the API returns JSON data
            data = response.json().get('data', []) # Extract 'data' list from JSON
            return render(request, 'home.html', {'data': data})
        else:
            # Handle API request error
            error = True
            message = "Failed to fetch data from external API."
            return render(request, 'home.html', {'message': message, 'error': error})
    
def userAnimeBrowse(request, keyword):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        # Make a request to the external API
        api_url = f'https://api.jikan.moe/v4/anime?q={keyword}'
        response = requests.get(api_url)
        
        if response.status_code == 200:
            # Assuming the API returns JSON data
            data = response.json().get('data', []) # Extract 'data' list from JSON
            return render(request, 'results.html', {'keyword': keyword, 'data': data})
        else:
            # Handle API request error
            error = True
            message = "Failed to fetch data from external API."
            return render(request, 'results.html', {'message': message, 'error': error})