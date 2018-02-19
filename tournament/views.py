from django.shortcuts import render,redirect
from .models import Team
from player.models import Player
# Create your views here.


def team(request):
    teams = Team.objects.all()
    context = {'teams': teams}
    return render(request, 'tournament/team.html', context)


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
    return redirect('tournament:team')
