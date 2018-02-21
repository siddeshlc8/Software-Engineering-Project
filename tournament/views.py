from django.shortcuts import render, redirect
from .models import Team, Tournament, Match
from player.models import Player
from .forms import TournamentCreationForm, TeamCreationForm,MatchCreationForm
from django.contrib import messages
# Create your views here.


def create_tournament(request):
    if request.method == 'POST':
        form = TournamentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tournament:tournament')
    else:
        form = TournamentCreationForm()
        context = {'form': form}
        return render(request, 'tournament/create_team.html', context)


def create_team(request, tournament_id):
    if request.method == 'POST':
        form = TeamCreationForm(request.POST)
        current_tournament = Tournament.objects.get(pk=tournament_id)
        if form.is_valid():
            team = form.save(commit=False)
            team.tournament = current_tournament
            team.save()
            return redirect('tournament:tournament_teams', tournament_id)
        else:
            messages.error(request, 'Please correct the error below.')
            return redirect('tournament:tournament_teams', tournament_id)
    else:
        form = TeamCreationForm()
        context = {'form': form}
        return render(request, 'tournament/create_tournament.html', context)


def tournament(request):
    all_tournament = Tournament.objects.all()
    context = {'all_tournament': all_tournament}
    return render(request, 'tournament/tournaments.html', context)


def tournament_teams(request, tournament_id):
    current_tournament = Tournament.objects.get(pk=tournament_id)
    teams = current_tournament.team_set.all()
    context = {'current_tournament': current_tournament, 'teams': teams}
    return render(request, 'tournament/tournament_teams.html', context)


def team_players(request, team_id):
    current_team = Team.objects.get(pk=team_id)
    current_players = current_team.player_set.all()
    available_players = Player.objects.exclude(team__pk=team_id)
    context = {'current_players': current_players, 'team': current_team, 'available_players': available_players}
    return render(request, 'tournament/team_players.html', context)


def team_players_add(request, team_id, player_id):
    team_ = Team.objects.get(pk=team_id)
    player_ = Player.objects.get(pk=player_id)
    team_.player_set.add(player_)
    return redirect('tournament:team_players', team_id)

def matches(request, tournament_id):
    tournament=Tournament.objects.get(id=tournament_id)
    all_matches = tournament.match_set.all()
    return render(request,'tournament/matches.html',{'tournament':tournament,'matches':all_matches})

def create_match(request,tournament_id):
    if request.method == 'POST':
        form = MatchCreationForm(request.POST)
        tournament = Tournament.objects.get(pk=tournament_id)
        if form.is_valid():
            match = form.save(commit=False)
            match.tournament = tournament
            match.winner=match.team_1
            match.save()
            return redirect('tournament:matches', tournament_id)
        else:
            messages.error(request, 'Please correct the error below.')
            return redirect('tournament:create_match', tournament_id)
    else:
        form = MatchCreationForm()
        context = {'form': form}
        return render(request, 'tournament/create_match.html', context)
