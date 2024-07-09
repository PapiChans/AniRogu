from django.conf import settings
from django.shortcuts import render, redirect
import requests

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