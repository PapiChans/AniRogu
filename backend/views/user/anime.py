from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
import requests, os

def backendAddAnime(request):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        # Extract query parameters from the request
        anime_number = request.GET.get('anime_number')
        anime_name = request.GET.get('anime_name')
        anime_picture = request.GET.get('anime_picture')

        user_id = request.user

        anime = Anime.objects.create(
            user_Id = user_id,
            anime_Number = anime_number,
            anime_Name = anime_name,
            anime_Picture = anime_picture,
            anime_Status = 'Not Started'
        )
        anime.save()

        # Necessary Data to Render new HTML
        api_url = f'https://api.jikan.moe/v4/anime/{anime_number}/full'
        response = requests.get(api_url)

        # Relations
        r_api_url = f'https://api.jikan.moe/v4/anime/{anime_number}/relations'
        r_response = requests.get(r_api_url)
        if response.status_code == 200 and r_response.status_code == 200:
            data = response.json().get('data', [])
            r_data = r_response.json().get('data', [])

            # Prepare a list to store fetched relation large_image_urls
            relation_details = []

            # Iterate through relations to fetch additional data
            for relation in r_data:
                for entry in relation.get('entry', []):
                    mal_id = entry.get('mal_id')
                    anime_api_url = f'https://api.jikan.moe/v4/anime/{mal_id}'
                    anime_response = requests.get(anime_api_url)

                    if anime_response.status_code == 200:
                        anime_data = anime_response.json().get('data', {})
                        large_image_url = anime_data.get('images', {}).get('webp', {}).get('large_image_url', '')

                        # Append fetched data to relation_details list
                        relation_details.append({
                            'large_image_url': large_image_url,
                            'relation': relation.get('relation'),
                            'entry_name': entry.get('name'),
                            'entry_url': entry.get('url')
                        })
                    
                # Check the Anime if it's already added by the user
                try:
                    anime =  Anime.objects.get(user_Id = request.user.user_Id,anime_Number = anime_number)
                    anime_added = True
                    status = 'success'
                    message = 'Add Anime Successfully'
                except Anime.DoesNotExist:
                    anime_added = False
                    status = 'error'
                    message = 'Add Anime Failed'

        return render(request, 'animeinfo.html', {'data': data, 'r_data': r_data, 'relation_details': relation_details, 'anime_added': anime_added, 'id': anime_number, 'status': status, 'message': message})
    
def backendRemoveAnime(request):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        # Extract query parameters from the request
        anime_number = request.GET.get('anime_number')
        
        anime =  Anime.objects.get(user_Id = request.user.user_Id,anime_Number = anime_number)
        anime.delete()

        # Necessary Data to Render new HTML
        api_url = f'https://api.jikan.moe/v4/anime/{anime_number}/full'
        response = requests.get(api_url)

        # Relations
        r_api_url = f'https://api.jikan.moe/v4/anime/{anime_number}/relations'
        r_response = requests.get(r_api_url)
        if response.status_code == 200 and r_response.status_code == 200:
            data = response.json().get('data', [])
            r_data = r_response.json().get('data', [])

            # Prepare a list to store fetched relation large_image_urls
            relation_details = []

            # Iterate through relations to fetch additional data
            for relation in r_data:
                for entry in relation.get('entry', []):
                    mal_id = entry.get('mal_id')
                    anime_api_url = f'https://api.jikan.moe/v4/anime/{mal_id}'
                    anime_response = requests.get(anime_api_url)

                    if anime_response.status_code == 200:
                        anime_data = anime_response.json().get('data', {})
                        large_image_url = anime_data.get('images', {}).get('webp', {}).get('large_image_url', '')

                        # Append fetched data to relation_details list
                        relation_details.append({
                            'large_image_url': large_image_url,
                            'relation': relation.get('relation'),
                            'entry_name': entry.get('name'),
                            'entry_url': entry.get('url')
                        })
                    
                # Check the Anime if it's already added by the user
                try:
                    anime =  Anime.objects.get(user_Id = request.user.user_Id,anime_Number = anime_number)
                    anime_added = True
                    status = 'error'
                    message = 'Remove Anime Failed'
                except Anime.DoesNotExist:
                    anime_added = False
                    status = 'success'
                    message = 'Remove Anime Successfully'

        return render(request, 'animeinfo.html', {'data': data, 'r_data': r_data, 'relation_details': relation_details, 'anime_added': anime_added, 'id': anime_number, 'status': status, 'message': message})