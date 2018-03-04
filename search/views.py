from django.shortcuts import render
from player.models import Player
from tournament.models import Team, Tournament
from .filters import PlayerFilter, TournamentFilter, TeamFilter, OrganizerFilter
from organizer.models import Organizer


def search(request):
    try:
        p = Player.objects.get(pk=request.user.id)
        context = {'P': p}
    except Exception:
        try:
            o = Organizer.objects.get(pk=request.user.id)
            context = {'O': o}
        except Exception:
            context = {'P': None}
    return render(request, 'search/search.html', context)


def search_tournaments(request):
    tournaments = Tournament.objects.all()
    tournaments_filter = TournamentFilter(request.GET, queryset=tournaments)
    try:
        player = Player.objects.get(pk=request.user.id)
        context = {'P': player, 'filter': tournaments_filter}
    except Exception:
        try:
            o = Organizer.objects.get(pk=request.user.id)
            context = {'O': o, 'filter': tournaments_filter}
        except Exception:
            context = {'P': None, 'filter': tournaments_filter}
    return render(request, 'search/search_tournaments.html', context)


def search_teams(request):
    teams = Team.objects.all()
    teams_filter = TeamFilter(request.GET, queryset=teams)
    try:
        player = Player.objects.get(pk=request.user.id)
        context = {'P': player, 'filter': teams_filter}
    except Exception:
        try:
            o = Organizer.objects.get(pk=request.user.id)
            context = {'O': o, 'filter': teams_filter}
        except Exception:
            context = {'P': None, 'filter': teams_filter}
    return render(request, 'search/search_teams.html', context)


def search_players(request):
    players = Player.objects.all()
    players_filter = PlayerFilter(request.GET, queryset=players)
    try:
        player = Player.objects.get(pk=request.user.id)
        context = {'players': players, 'P': player, 'filter': players_filter}
    except Exception:
        try:
            o = Organizer.objects.get(pk=request.user.id)
            context = {'players': players, 'O': o, 'filter': players_filter}
        except Exception:
            context ={'players': players, 'P': None, 'filter': players_filter}
    return render(request, 'search/search_players.html', context)


def search_organizers(request):
    organizers = Organizer.objects.all()
    organizers_filter = OrganizerFilter(request.GET, queryset=organizers)
    try:
        player = Player.objects.get(pk=request.user.id)
        context = {'organizers': organizers, 'P': player, 'filter': organizers_filter}
    except Exception:
        try:
            o = Organizer.objects.get(pk=request.user.id)
            context = {'organizers': organizers, 'O': o, 'filter': organizers_filter}
        except Exception:
            context = {'organizers': organizers, 'P': None, 'filter': organizers_filter}
    return render(request, 'search/search_organizers.html', context)


def player_details(request, player_id):
    player = Player.objects.get(pk=player_id)
    all_details = player.details()
    try:
        P = Player.objects.get(pk=request.user.id)
        context = {'all_details': all_details, 'P': P}
    except Exception:
        try:
            o = Organizer.objects.get(pk=request.user.id)
            context = {'all_details': all_details, 'O': o}
        except Exception:
            context = {'all_details': all_details, 'O': None}
    return render(request, 'search/player_details.html', context)


def tournaments_details(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    try:
        P = Player.objects.get(pk=request.user.id)
        context = {'tournament': tournament, 'P': P}
    except Exception:
        try:
            o = Organizer.objects.get(pk=request.user.id)
            context = {'tournament': tournament, 'O': o}
        except Exception:
            context = {'tournament': tournament, 'O': None}
    return render(request, 'search/tournaments_details.html', context)


def teams_details(request, team_id):
    team = Team.objects.get(pk=team_id)
    try:
        P = Player.objects.get(pk=request.user.id)
        context = {'team': team, 'P': P}
    except Exception:
        try:
            o = Organizer.objects.get(pk=request.user.id)
            context = {'team': team, 'O': o}
        except Exception:
            context = {'team': team, 'O': None}
    return render(request, 'search/teams_details.html', context)