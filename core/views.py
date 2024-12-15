from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . models import Movie, MovieList
from django.contrib.auth import authenticate
from django.contrib import messages, auth

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import re


# Create your views here.
@login_required(login_url='login')
def index(request):
    movies = Movie.objects.all()
    genres = dict(Movie.GENRE_CHOICES)
    print(movies)
    context = {
        'genres': genres,
        'movies': movies,
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def movie(request, pk):
    movie_uid = pk
    movie_details = Movie.objects.get(u_id=movie_uid)
    context = {
        'movie_details': movie_details,
    }

    return render(request, 'movie.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        # If user is real/present
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Credentials donot match!!')
            return redirect('login')
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        #user = User.objects.filter(usename=username)
        if password2 != password:
            messages.info(request, "Password donot match!!")
            return redirect('signup')
        else:
            if User.objects.filter(email=email).exists():
                messages.info(request, "This email has already been used!!")
                return redirect('signup')

            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken!!")
                return redirect('signup')

            else:
                user = User.objects.create(email=email, username=username, password=password)
                user.set_password(password)
                user.save()
                # Loggin in user automatically
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('index')
    return render(request, 'signup.html')


@login_required(login_url='login')
def my_list(request):
    movie_list = MovieList.objects.filter(owner_user=request.user)
    #print(movie_list)
    user_movie_list=[]
    for movie in movie_list:
        user_movie_list.append(movie.movie)
    context = {
        'movies':user_movie_list,
    }
    return render(request, 'my_list.html', context)


@login_required(login_url='login')
def add_to_list(request):
    if request.method == 'POST':
        movie_url_id = request.POST.get('movie_id')
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, movie_url_id)
        movie_id = match.group() if match else None

        movie = get_object_or_404(Movie, u_id=movie_id)
        movie_list, created = MovieList.objects.get_or_create(owner_user=request.user, movie=movie)

        if created:
            response_data = {'status': 'success', 'message': 'Added ✓'}
        else:
            response_data = {'status': 'info', 'message': 'Movie already in list'}

        return JsonResponse(response_data)

    else:
        # return error
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')