from django.conf import settings
from django.shortcuts import render, redirect
import requests, os
from datetime import datetime
from backend.models import *

# Create your views here.
def userHome(request):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        return render(request, 'home.html')
    
def userAnimeBrowse(request, keyword, page):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        # Make a request to the external API
        api_url = f'https://api.jikan.moe/v4/anime?q={keyword}&page={page}'
        response = requests.get(api_url)

        # Genre URL
        genre_url = f'https://api.jikan.moe/v4/genres/anime'
        genre_response = requests.get(genre_url)

        if response.status_code == 200 and genre_response.status_code == 200:
            data = response.json().get('data', [])
            pagination = response.json().get('pagination', {})

            current_page = pagination.get('current_page', 1)
            last_visible_page = pagination.get('last_visible_page', 1)
            has_next_page = pagination.get('has_next_page', False)

            # Calculate the range of pages to display
            page_range = range(1, last_visible_page + 1)

            #Genre
            genre = genre_response.json().get('data',[])

            context = {
                'keyword': keyword,
                'data': data,
                'current_page': current_page,
                'last_visible_page': last_visible_page,
                'has_next_page': has_next_page,
                'page_range': page_range,

                # Genre
                'genre': genre,
            }

            return render(request, 'results.html', context)
        else:
            # Handle API request error
            error = True
            message = "Failed to fetch data from external API."
            return render(request, 'results.html', {'message': message, 'error': error})
        
def userAnimeGenre(request, genres, page):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        # Genre URL
        genre_url = f'https://api.jikan.moe/v4/genres/anime'
        genre_response = requests.get(genre_url)

        if genre_response.status_code == 200:
            #Genre
            genre_list = genre_response.json().get('data',[])

            # Find the selected genre by name and retrieve its mal_id
            selected_genre = None
            for g in genre_list:
                if g['name'].lower() == genres.lower():
                    selected_genre = g
                    break

            if selected_genre:
                mal_id = selected_genre['mal_id']

            api_url = f'https://api.jikan.moe/v4/anime?genres={mal_id}&page={page}'
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json().get('data', [])
                pagination = response.json().get('pagination', {})

                current_page = pagination.get('current_page', 1)
                last_visible_page = pagination.get('last_visible_page', 1)
                has_next_page = pagination.get('has_next_page', False)

                # Calculate the range of pages to display
                page_range = range(1, last_visible_page + 1)


            context = {
                'genres': genres,
                'page': page,
                'genre': genre_list,

                # For Pagination
                'data': data,
                'current_page': current_page,
                'last_visible_page': last_visible_page,
                'has_next_page': has_next_page,
                'page_range': page_range,
            }
            return render(request, 'genre.html', context)
        else:
            # Handle API request error
            error = True
            message = "Failed to fetch data from external API."
            return render(request, 'genre.html', {'message': message, 'error': error})
        
def userAnimeUpcoming(request, page):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        # Genre URL
        genre_url = f'https://api.jikan.moe/v4/genres/anime'
        genre_response = requests.get(genre_url)

        api_url = f'https://api.jikan.moe/v4/seasons/upcoming?page={page}'
        response = requests.get(api_url)

        if genre_response.status_code == 200 and response.status_code == 200:
            #Genre
            genre_list = genre_response.json().get('data',[])

            data = response.json().get('data', [])
            pagination = response.json().get('pagination', {})

            current_page = pagination.get('current_page', 1)
            last_visible_page = pagination.get('last_visible_page', 1)
            has_next_page = pagination.get('has_next_page', False)

            # Calculate the range of pages to display
            page_range = range(1, last_visible_page + 1)

            context = {
                'page': page,
                'genre': genre_list,

                # For Pagination
                'data': data,
                'current_page': current_page,
                'last_visible_page': last_visible_page,
                'has_next_page': has_next_page,
                'page_range': page_range,
            }
            return render(request, 'upcoming.html', context)
        else:
            # Handle API request error
            error = True
            message = "Failed to fetch data from external API."
            return render(request, 'upcoming.html', {'message': message, 'error': error})
        
def userAnimeInfo(request, id):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        api_url = f'https://api.jikan.moe/v4/anime/{id}/full'
        response = requests.get(api_url)

        # Relations
        r_api_url = f'https://api.jikan.moe/v4/anime/{id}/relations'
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
                    anime =  Anime.objects.get(user_Id = request.user.user_Id,anime_Number = id)
                    anime_added = True
                except Anime.DoesNotExist:
                    anime_added = False

            return render(request, 'animeinfo.html', {'data': data, 'r_data': r_data, 'relation_details': relation_details, 'anime_added': anime_added, 'id': id})
        else:
            # Handle API request error
            error = True
            message = "Failed to fetch data from external API."
            return render(request, 'home.html', {'message': message, 'error': error})
        
def userAbout(request):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        template_path = os.path.join(settings.BASE_DIR, 'user/templates/about.html')
        modified_time = os.path.getmtime(template_path)
        modified_time = datetime.fromtimestamp(modified_time)
        formatted_date = modified_time.strftime('%B %d, %Y - %I:%M %p')
        context = {
            'last_modified_time': formatted_date,
        }
        return render(request, 'about.html', context)

def userProfile(request):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        user = User.objects.get(user_Id = request.user.user_Id)
        context = {
            'profile_name': user.profile_name,
        }
        return render(request, 'profile.html', context)

def userAnimeList(request):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        anime = Anime.objects.filter(user_Id = request.user.user_Id).order_by('anime_Name')
        not_started = Anime.objects.filter(user_Id = request.user.user_Id, anime_Status = 'Not Started').order_by('anime_Name')
        in_progress = Anime.objects.filter(user_Id = request.user.user_Id, anime_Status = 'In Progress').order_by('anime_Name')
        completed = Anime.objects.filter(user_Id = request.user.user_Id, anime_Status = 'Completed').order_by('anime_Name')
        context = {
            'anime': anime,
            'not_started': not_started,
            'in_progress': in_progress,
            'completed': completed,
        }
        return render(request, 'animelist.html', context)
    
def userAnimeEpisode(request, anime_Id):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        # Check User
        user = User.objects.get(user_Id = request.user.user_Id)
        anime = Anime.objects.get(anime_Id = anime_Id)
        the_user_id = user.user_Id
        the_user_id_anime = anime.user_Id.user_Id
        if the_user_id != the_user_id_anime:
            context = {
                'error': True,
                'message': 'Access Denied',
            }
            return render(request, 'home.html', context)
        else:
            episode = AnimeEpisode.objects.filter(anime_Id = anime_Id).order_by('episode_Number')
            context = {
                'anime': anime,
                'episode': episode,
            }
            return render(request, 'animeepisode.html', context)