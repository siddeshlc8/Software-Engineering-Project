from django.shortcuts import render, redirect
from .forms import PlayerProfileForm
from .models import Player
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from performance.models import BattingInnings, BowlingInnings, PerformanceTotal
from tournament.models import Team, Match, Tournament
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def player_home(request):
    if request.user.username:
        user = Player.objects.get(pk=request.user)
        context = {'P': user}
        return render(request, 'player/home.html', context)
    else:
        return redirect('login')


def player_performance(request):
    try:
        player = Player.objects.get(pk=request.user.id)
        data1 = BattingInnings.objects.filter(player=player)
        data2 = BowlingInnings.objects.filter(player=player)
        labels = []
        values = []
        labels1 = []
        values1 = []
        for key in data1:
            labels.append(key.id)
            values.append(key.batting_runs)
        for key in data2:
            labels1.append(key.id)
            values1.append(key.wickets)
        total_data = PerformanceTotal.objects.get(player=player)
        context = {'labels': labels, 'values': values, 'labels1': labels1, 'values1': values1, 'total_data': total_data}
        return render(request, 'player/performance.html', context)
    except Exception:
        return redirect('login')


def player_view_profile(request):
    if request.user.username :
        user = Player.objects.get(pk=request.user)
        # player = vars(user) to list all attributes
        player = user.profile()
        context = {'player': player, 'P': user}
        return render(request, 'player/view_profile.html', context)
    else:
        return redirect('login')


def player_edit_profile(request):
    if request.user.username:
        player = Player.objects.get(pk=request.user.id)
        if request.method == 'POST':
            form = PlayerProfileForm(request.POST, request.FILES, instance=player)
            if form.is_valid():
                form.save()
                messages.success(request,'successfully edited your profile !')
                return redirect('player:player_view_profile')
        else:
            form = PlayerProfileForm(instance=player)
            context = {'form': form, 'P': player}
            return render(request, 'player/edit_profile.html', context)
    else:
        return redirect('login')


def player_change_password(request):
    if request.user.username:
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'successfully changed your password !')
                return redirect('player:player_home')
            else:
                messages.error(request, 'Please correct the error below.')
                return redirect('player:player_change_password')
        else:
            form = PasswordChangeForm(user=request.user)
            context = {'form': form, 'P': Player.objects.get(pk=request.user.id)}
            return render(request, 'player/change_password.html', context)
    else:
        return redirect('login')


def player_change_password_done(request):
    if request.user.username:
        context = {'P': Player.objects.get(pk=request.user.id)}
        return render(request, 'player/change_password_done.html', context)
    return redirect('login')


def my_tournaments(request):
    try:
        player = Player.objects.get(pk=request.user.id)
        player = Player.objects.get(pk=request.user.id)
        match = Match.objects.all()
        team = Team.objects.all()
        tournament = Tournament.objects.all()
        teams = []
        for t in team:
            players = t.players.all()
            for p in players:
                if p == player:
                    teams.append(t)

        matches = []
        for m in match:
            for t in teams:
                if m.team_1 == t:
                    matches.append(m)
                elif m.team_2 == t:
                    matches.append(m)

        tournaments = []
        for t in tournament:
            for m in matches:
                if m.tournament == t:
                    tournaments.append(t)

        context = {'tournaments': tournaments}
        return render(request, 'player/my_tournaments.html', context)
    except Exception:
        return redirect('login')


def my_matches(request):
    try:
        player = Player.objects.get(pk=request.user.id)
        match = Match.objects.all()
        team = Team.objects.all()
        teams = []
        for t in team:
            players = t.players.all()
            for p in players:
                if p == player:
                    teams.append(t)

        matches = []
        for m in match:
            for t in teams:
                if m.team_1 == t:
                    matches.append(m)
                elif m.team_2 == t:
                    matches.append(m)

        context = {'matches': matches}
        return render(request, 'player/my_matches.html', context)
    except Exception:
        return redirect('login')



