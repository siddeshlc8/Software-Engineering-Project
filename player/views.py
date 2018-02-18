from django.shortcuts import render, redirect
from .forms import PlayerSignUpForm
from django.contrib.auth import authenticate, login, logout
from .models import Player


# Create your views here.

def players_page(request):
    return render(request, 'player/player_page.html')


def player_home(request):
    return render(request, 'player/home.html')


def player_signup(request):
    if request.method == 'POST':
        form = PlayerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'player/registration/signup.html')
    else:
        form = PlayerSignUpForm()
    return render(request, 'player/registration/signup.html', {'form': form})


def player_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('player:player_home')
    return render(request, 'player/registration/login.html')


def player_logout(request):
    logout(request)
    return redirect('player:player_login')

