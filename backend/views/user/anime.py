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

         # Fetch episode data from Jikan API
        epi_url = f'https://api.jikan.moe/v4/anime/{anime_number}/episodes'
        epi_response = requests.get(epi_url)
        episode_data = epi_response.json()

        # Iterate over the episodes and save them
        for episode in episode_data['data']:
            add_episode = AnimeEpisode.objects.create(
                anime_Id= anime,
                episode_Number=episode['mal_id'],
                episode_Name=episode['title'],
                episode_Status='Not Started'  # Default status, you can adjust as needed
            )
            add_episode.save()

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

        anime_episode = AnimeEpisode.objects.filter(anime_Id = anime.anime_Id)
        anime_episode.delete()
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
    
def backendRemoveAnime2(request, anime_Id):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        fetchEpisodes = AnimeEpisode.objects.filter(anime_Id = anime_Id)
        fetchEpisodes.delete()
        fetchAnime = Anime.objects.get(anime_Id = anime_Id)
        fetchAnime.delete()

        anime = Anime.objects.filter(user_Id = request.user.user_Id).order_by('anime_Name')
        not_started = Anime.objects.filter(user_Id = request.user.user_Id, anime_Status = 'Not Started').order_by('anime_Name')
        in_progress = Anime.objects.filter(user_Id = request.user.user_Id, anime_Status = 'In Progress').order_by('anime_Name')
        completed = Anime.objects.filter(user_Id = request.user.user_Id, anime_Status = 'Completed').order_by('anime_Name')
        context = {
            'anime': anime,
            'not_started': not_started,
            'in_progress': in_progress,
            'completed': completed,
            'success': True,
            'message': 'Removed Anime Successfully'
        }
        return render(request, 'animelist.html', context)
    
def backendWatchingEpisode(request, episode_Id):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        EditEpisode = AnimeEpisode.objects.get(episode_Id = episode_Id)
        EditEpisode.episode_Status = 'Watching'
        EditEpisode.save()

        anime = EditEpisode.anime_Id
        anime.anime_Status = 'In Progress'
        anime.save()
        episode = AnimeEpisode.objects.filter(anime_Id = anime).order_by('episode_Number')
        context = {
            'anime': anime,
            'episode': episode,
            'success': True,
            'message': 'Update Episode Successfully'
        }
        return render(request, 'animeepisode.html', context)
    
def backendCompletedEpisode(request, episode_Id):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        EditEpisode = AnimeEpisode.objects.get(episode_Id = episode_Id)
        EditEpisode.episode_Status = 'Completed'
        EditEpisode.save()

        anime = EditEpisode.anime_Id

        # Retrieve all episodes related to this Anime
        total_episodes = AnimeEpisode.objects.filter(anime_Id=anime).count()
        completed_episodes = AnimeEpisode.objects.filter(anime_Id=anime, episode_Status='Completed').count()

        # Check if all episodes are completed
        all_completed = (total_episodes == completed_episodes)

        # Update the anime status based on episodes' status
        anime_status = 'Completed' if all_completed else 'In Progress'
        anime.anime_Status = anime_status
        anime.save()

        episode = AnimeEpisode.objects.filter(anime_Id = anime).order_by('episode_Number')
        context = {
            'anime': anime,
            'episode': episode,
            'success': True,
            'message': 'Update Episode Successfully'
        }
        return render(request, 'animeepisode.html', context)

def backendAnimeMarkAsCompleted(request, anime_Id):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        anime = Anime.objects.get(anime_Id = anime_Id)
        anime.anime_Status = 'Completed'
        anime.save()

        all_episodes = AnimeEpisode.objects.filter(anime_Id = anime_Id)
        for edit_episode in all_episodes:
            edit_episode.episode_Status = 'Completed'
            edit_episode.save()
        
        episode = AnimeEpisode.objects.filter(anime_Id = anime_Id).order_by('episode_Number')
        context = {
            'anime': anime,
            'episode': episode,
            'success': True,
            'message': 'Update Anime Successfully'
        }
        return render(request, 'animeepisode.html', context)
