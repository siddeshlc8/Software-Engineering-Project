from django.shortcuts import render, redirect
from .forms import PlayerSignUpForm, PlayerProfileForm
from django.contrib.auth import authenticate, login, logout
from .models import Player
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, LoginView, LogoutView, TemplateView
from django.views.generic import *


# Create your views here.
class PlayerPageView(TemplateView):
    template_name = 'player/player_page.html'


class PlayerBrowseView(ListView):
    model = Player
    context_object_name = 'all_players'
    template_name = 'player/browse_player.html'


def player_details(request, player_id):
    player = Player.objects.get(pk=player_id)
    all_details = player.details()
    context = {'all_details': all_details}
    return render(request, 'player/player_details.html', context)


class PlayerHomeView(TemplateView):
    template_name = 'player/home.html'


def player_signup(request):
    if request.method == 'POST':
        form = PlayerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'player/registration/login.html')
    else:
        form = PlayerSignUpForm()
    return render(request, 'player/registration/signup.html', {'form': form})


class PlayerLoginView(LoginView):
    template_name = 'player/registration/login.html'
    extra_context = {'next': '/player/home/'}


class PlayerLogoutView(LogoutView):
    next_page = '/player/login/'


def player_view_profile(request):
    if request.user.username :
        user = Player.objects.get(pk=request.user)
        # player = vars(user) to list all attributes
        player = user.profile()
        context = {'player': player}
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
            context = {'form': form}
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
            return render(request, 'player/change_password.html', {'form': form})
    else:
        return redirect('player:player_login')


def player_change_password_done(request):
    if request.user.username:
        return render(request, 'player/change_password_done.html')
    return redirect('player:player_login')


def players_page(request):
    all_players = Player.objects.all()
    context = {'all_players': all_players}
    return render(request, 'player/player_page.html', context)


def player_home(request):
    if request.user.username:
        return render(request, 'player/home.html')
    else:
        return redirect('player:player_login')


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