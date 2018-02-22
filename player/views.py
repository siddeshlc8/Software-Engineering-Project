from django.shortcuts import render, redirect
from .forms import PlayerSignUpForm, PlayerProfileForm
from django.contrib.auth import authenticate, login, logout
from .models import Player
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, LoginView, LogoutView, TemplateView
from django.views.generic import *
from tournament.models import Team, Tournament
from .filters import PlayerFilter, TournamentFilter, TeamFilter


# Create your views here.
class PlayerPageView(TemplateView):
    template_name = 'player/player_page.html'


def player_details(request, player_id):
    try:
        P = Player.objects.get(pk=request.user.id)
    except Exception:
        P=None
    player = Player.objects.get(pk=player_id)
    all_details = player.details()
    context = {'all_details': all_details, 'P': P}
    return render(request, 'player/player_details.html', context)


def player_home(request):
    if request.user.username:
        user = Player.objects.get(pk=request.user)
        context = {'P': user}
        return render(request, 'player/home.html', context)
    else:
        return redirect('player:player_login')


def player_performance(request):
    if request.user.username:
        context = {'P': Player.objects.get(pk=request.user.id)}
        return render(request, 'player/performance.html', context)
    else:
        return redirect('player:player_login')


def player_signup(request):
    if request.method == 'POST':
        form = PlayerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'player/login.html')
    else:
        form = PlayerSignUpForm()
    return render(request, 'player/signup.html', {'form': form})


class PlayerLogoutView(LogoutView):
    next_page = '/player/login/'


def player_view_profile(request):
    if request.user.username :
        user = Player.objects.get(pk=request.user)
        # player = vars(user) to list all attributes
        player = user.profile()
        context = {'player': player, 'P': user}
        return render(request, 'player/view_profile.html', context)
    else:
        return redirect('player:player_login')


def player_edit_profile(request):
    if request.user.username:
        player = Player.objects.get(pk=request.user.id)
        if request.method == 'POST':
            form = PlayerProfileForm(request.POST, instance=player)
            if form.is_valid():
                form.save()
                return redirect('player:player_view_profile')
        else:
            form = PlayerProfileForm(instance=player)
            context = {'form': form, 'P': player}
            return render(request, 'player/edit_profile.html', context)
    else:
        return redirect('player:player_login')


def player_change_password(request):
    if request.user.username:
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('player:player_change_password_done')
            else:
                messages.error(request, 'Please correct the error below.')
                return redirect('player:player_change_password')
        else:
            form = PasswordChangeForm(user=request.user)
            context = {'form': form, 'P': Player.objects.get(pk=request.user.id)}
            return render(request, 'player/change_password.html', context)
    else:
        return redirect('player:player_login')


def player_change_password_done(request):
    if request.user.username:
        context = {'P': Player.objects.get(pk=request.user.id)}
        return render(request, 'player/change_password_done.html', context)
    return redirect('player:player_login')


def search(request):
    tournaments = Tournament.objects.all()
    teams = Team.objects.all()
    context = {'tournaments': tournaments, 'teams': teams, 'P': Player.objects.get(pk=request.user.id)}
    return render(request, 'player/search.html', context)


def search_tournaments(request):
    try:
        player = Player.objects.get(pk=request.user.id)
    except Exception:
        player = None
    tournaments = Tournament.objects.all()
    tournaments_filter = TournamentFilter(request.GET, queryset=tournaments)
    context = {'P': player, 'filter': tournaments_filter}
    return render(request, 'player/search_tournaments.html', context)


def search_teams(request):
    try:
        player = Player.objects.get(pk=request.user.id)
    except Exception:
        player = None
    teams = Team.objects.all()
    teams_filter = TeamFilter(request.GET, queryset=teams)
    context = {'P': player, 'filter': teams_filter}
    return render(request, 'player/search_teams.html', context)


def search_players(request):
    try:
        player = Player.objects.get(pk=request.user.id)
    except Exception:
        player = None
    players = Player.objects.all()
    players_filter = PlayerFilter(request.GET, queryset=players)
    context = {'players': players, 'P': player, 'filter': players_filter}
    return render(request, 'player/search_players.html', context)


def tournaments_details(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    context = {'tournament': tournament, 'P': Player.objects.get(pk=request.user.id)}
    return render(request, 'player/tournaments_details.html', context)


def teams_details(request, team_id):
    team = Team.objects.get(pk=team_id)
    context = {'team': team, 'P': Player.objects.get(pk=request.user.id)}
    return render(request, 'player/teams_details.html', context)


def players_page(request):
    all_players = Player.objects.all()
    context = {'all_players': all_players}
    return render(request, 'player/player_page.html', context)


def player_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                Player.objects.get(pk=request.user)
            except Exception:
                return redirect('player:player_login')
            return redirect('player:player_home')
    return render(request, 'player/login.html')


def player_logout(request):
    logout(request)
    return redirect('player:player_login')