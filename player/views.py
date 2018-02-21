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


# Create your views here.
class PlayerPageView(TemplateView):
    template_name = 'player/Before_Login/player_page.html'


class PlayerBrowseView(ListView):
    model = Player
    context_object_name = 'all_players'
    template_name = 'player/Before_Login/browse_player.html'


def player_details(request, player_id):
    if request.user.username:
        player = Player.objects.get(pk=player_id)
        all_details = player.details()
        context = {'all_details': all_details}
        return render(request, 'player/After_Login/player_details.html', context)
    else:
        player = Player.objects.get(pk=player_id)
        all_details = player.details()
        context = {'all_details': all_details}
        return render(request, 'player/Before_Login/player_details.html', context)


def player_home(request):
    if request.user.username:
        user = Player.objects.get(pk=request.user)
        context = {'user': user}
        return render(request, 'player/After_Login/home.html', context)
    else:
        return redirect('player:player_login')


class PlayerPerformanceView(TemplateView):
    template_name = 'player/After_Login/performance.html'


def player_signup(request):
    if request.method == 'POST':
        form = PlayerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'player/registration/login.html')
    else:
        form = PlayerSignUpForm()
    return render(request, 'player/registration/signup.html', {'form': form})


class PlayerLogoutView(LogoutView):
    next_page = '/player/login/'


def player_view_profile(request):
    if request.user.username :
        user = Player.objects.get(pk=request.user)
        # player = vars(user) to list all attributes
        player = user.profile()
        context = {'player': player}
        return render(request, 'player/After_Login/view_profile.html', context)
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
            context = {'form': form}
            return render(request, 'player/After_Login/edit_profile.html', context)
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
            return render(request, 'player/After_Login/change_password.html', {'form': form})
    else:
        return redirect('player:player_login')


def player_change_password_done(request):
    if request.user.username:
        return render(request, 'player/After_Login/change_password_done.html')
    return redirect('player:player_login')


def search(request):
    tournaments = Tournament.objects.all()
    teams = Team.objects.all()
    context = {'tournaments': tournaments, 'teams': teams}
    return render(request, 'player/After_Login/search.html', context)


def search_tournaments(request):
    tournaments = Tournament.objects.all()
    context = {'tournaments': tournaments}
    return render(request, 'player/After_Login/search_tournaments.html', context)


def search_teams(request):
    teams = Team.objects.all()
    context = {'teams': teams}
    return render(request, 'player/After_Login/search_teams.html', context)


def search_players(request):
    if request.user.username:
        players = Player.objects.all()
        context = {'players': players}
        return render(request, 'player/After_Login/search_players.html', context)
    else:
        players = Player.objects.all()
        context = {'players': players}
        return render(request, 'player/Before_Login/browse_player.html', context)


def tournaments_details(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    context = {'tournament': tournament}
    return render(request, 'player/After_Login/tournaments_details.html', context)


def teams_details(request, team_id):
    team = Team.objects.get(pk=team_id)
    context = {'team': team}
    return render(request, 'player/After_Login/teams_details.html', context)


def players_page(request):
    all_players = Player.objects.all()
    context = {'all_players': all_players}
    return render(request, 'player/Before_Login/player_page.html', context)


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
    return render(request, 'player/registration/login.html')


def player_logout(request):
    logout(request)
    return redirect('player:player_login')