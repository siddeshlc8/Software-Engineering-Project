from django.contrib import messages

from player.forms import PlayerSignUpForm
from django.contrib.auth import authenticate, login, logout
from player.models import Player
from django.shortcuts import render, redirect
from organizer.form import OrganizerSignupForm
from organizer.models import Organizer
from tournament.models import Tournament ,Match


def organizers_page(request):
    all_organizers=Organizer.objects.all()
    return render(request, 'cricket/organizers_page.html', {'all_organizers' : all_organizers})


def home_page(request):
    return render(request, 'cricket/home.html')


def players_page(request):
    all_players = Player.objects.all()
    context = {'all_players': all_players}
    return render(request, 'cricket/player_page.html', context)


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                Player.objects.get(pk=request.user)
                return redirect('player:player_home')
            except Exception:
                try:
                    Organizer.objects.get(pk=request.user)
                    messages.success(request, 'You have  successfully logged in!')
                    return redirect('organizer:home')
                except Exception:
                        return redirect('login')
        else:
            messages.warning(request, 'Incorrect username or password !')
            render(request, 'cricket/login.html')

    return render(request, 'cricket/login.html')


def player_signup(request):
    if request.method == 'POST':
        form = PlayerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'cricket/login.html')
    else:
        form = PlayerSignUpForm()
    return render(request, 'cricket/player_signup.html', {'form': form})


def organizer_signup(request):
    if request.method=='POST':
        form=OrganizerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('organizer:home')
        else:
            return render(request, 'cricket/organizer_signup.html', {'form': form,'errors':form.errors})
    else:
         form=OrganizerSignupForm()
    return render(request, 'cricket/organizer_signup.html', {'form':form})


def signout(request):
    logout(request)
    messages.success(request, 'You have  successfully logged out!')

    return redirect('login')

def live(request):
    match =Match.objects.filter(match_status=1)
    tournament=Tournament.objects.filter(tournament_status=1)
    return  render(request,'cricket/live.html',{'matches':match,'tournaments':tournament})

