from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . models import Movie
from django.contrib.auth import authenticate
from django.contrib import messages, auth


# Create your views here.
def index(request):
    movies = Movie.objects.all()
    genres = dict(Movie.GENRE_CHOICES)
    context = {
        'genres': genres,
        'movies': movies,
    }
    return render(request, 'index.html', context)

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