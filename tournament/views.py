from django.shortcuts import render,redirect
from .models import Team, Tournament
from player.models import Player
from .forms import TournamentCreationForm
# Create your views here.


def create_tournament(request):
    form = TournamentCreationForm()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('tournament:tournament')
    else:
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
    return redirect('tournament:team')
