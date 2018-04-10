from django.shortcuts import render, redirect
from player.models import Player
from tournament.models import Team, Tournament, Match, Score, FirstInningss, SecondInnings, MatchAdditional
from .filters import PlayerFilter, TournamentFilter, TeamFilter, OrganizerFilter
from organizer.models import Organizer
from performance.models import BattingInnings, BowlingInnings
from performance.models import PerformanceTotal


def player(request, id):
    try:
        P = Player.objects.get(pk=request.user.id)
        context = {'P': P}
    except Exception:
        try:
            o = Organizer.objects.get(pk=request.user.id)
            context = { 'O': o}
        except Exception:
            context = {'O': None}
    try:
        player = Player.objects.get(pk=id)
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
        context.update({'labels': labels, 'values': values, 'labels1': labels1, 'values1': values1, 'total_data': total_data})
        return render(request, 'search/performance_matches.html', context)
    except Exception:
        return redirect('login')


def nav_search_matches(request):
    if request.method == 'GET':
        try:
            p = Player.objects.get(pk=request.user.id)
            context = {'P': p}
        except Exception:
            try:
                o = Organizer.objects.get(pk=request.user.id)
                context = {'O': o}
            except Exception:
                context = {'P': None}
        query = request.GET.get("q")
        matches = Match.objects.filter(name__icontains=query).order_by('name')
        context.update({'matches': matches})
        return render(request, 'search/nav_search_matches.html', context)


def nav_search_players(request):
    if request.method == 'GET':
        try:
            p = Player.objects.get(pk=request.user.id)
            context = {'P': p}
        except Exception:
            try:
                o = Organizer.objects.get(pk=request.user.id)
                context = {'O': o}
            except Exception:
                context = {'P': None}
        query = request.GET.get("q")
        players = Player.objects.filter(first_name__contains=query).order_by('first_name')
        context.update({'players': players})
        return render(request, 'search/nav_search_players.html', context)


def nav_search_organizers(request):
    if request.method == 'GET':
        try:
            p = Player.objects.get(pk=request.user.id)
            context = {'P': p}
        except Exception:
            try:
                o = Organizer.objects.get(pk=request.user.id)
                context = {'O': o}
            except Exception:
                context = {'P': None}
        query = request.GET.get("q")
        organizers = Organizer.objects.filter(first_name__contains=query)
        context.update({'organizers': organizers})
        return render(request, 'search/nav_search_organizers.html', context)


def nav_search_teams(request):
    if request.method == 'GET':
        try:
            p = Player.objects.get(pk=request.user.id)
            context = {'P': p}
        except Exception:
            try:
                o = Organizer.objects.get(pk=request.user.id)
                context = {'O': o}
            except Exception:
                context = {'P': None}
        query = request.GET.get("q")
        teams = Team.objects.filter(name__contains= query).order_by('name')
        context.update({'teams': teams})
        return render(request, 'search/nav_search_teams.html', context)


def nav_search_tournaments(request):
    if request.method == 'GET':
        try:
            p = Player.objects.get(pk=request.user.id)
            context = {'P': p}
        except Exception:
            try:
                o = Organizer.objects.get(pk=request.user.id)
                context = {'O': o}
            except Exception:
                context = {'P': None}
        query = request.GET.get("q")
        tournaments = Tournament.objects.filter(name__contains= query).order_by('name')
        context.update({'tournaments': tournaments})
        return render(request, 'search/nav_search_tournaments.html', context)


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
        context = {'all_details': all_details,'player':player ,'P': P}
    except Exception:
        try:
            o = Organizer.objects.get(pk=request.user.id)
            context = {'all_details': all_details, 'player':player ,'O': o}
        except Exception:
            context = {'all_details': all_details,'player':player , 'O': None}
    return render(request, 'search/player_details.html', context)


def tournaments_details(request, tournament_id):
    current_tournament = Tournament.objects.get(pk=tournament_id)
    teams = current_tournament.team_set.all()
    context = {'current_tournament': current_tournament, 'teams': teams}
    try:
        P = Player.objects.get(pk=request.user.id)
        context.update({'current_tournament': current_tournament, 'teams': teams, 'P': P})
    except Exception:
        try:
            o = Organizer.objects.get(pk=request.user.id)
            context = {'current_tournament': current_tournament, 'teams': teams, 'O': o}
        except Exception:
            context.update({'current_tournament': current_tournament, 'teams': teams, 'O': None})
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


def match_details(request, match_id):
    match = Match.objects.get(pk=match_id)
    try:
        P = Player.objects.get(pk=request.user.id)
        context = {'match': match, 'P': P}
    except Exception:
        try:
            o = Organizer.objects.get(pk=request.user.id)
            context = {'match': match, 'O': o}
        except Exception:
            context = {'match': match, 'O': None}
    match = Match.objects.get(id=match_id)
    match_additional = MatchAdditional.objects.get(match=match)
    innings = match_additional.current_innings

    if innings == 'First':
        current_innings = FirstInningss.objects.get(match=match)
        bowling_team = current_innings.bowling_team
        batting_team = current_innings.batting_team
    else:
        current_innings = SecondInnings.objects.get(match=match)
        bowling_team = current_innings.bowling_team
        batting_team = current_innings.batting_team

    commentary_first_innings = Score.objects.filter(match=match).filter(innings='First').order_by(
        'over_number')
    commentary_second_innings = Score.objects.filter(match=match).filter(innings='Second').order_by(
        'over_number')

    team_batting = FirstInningss.objects.get(match=match)
    team_bowling = team_batting.bowling_team
    team_batting = team_batting.batting_team

    innings1_batting = BattingInnings.objects.filter(match=match).filter(team=team_batting).filter(
        played=True).order_by('started_time')

    innings1_bowling = BowlingInnings.objects.filter(match=match).filter(team=team_bowling).filter(
        played=True).order_by('started_time')

    innings2_batting = BattingInnings.objects.filter(match=match).filter(team=team_bowling).filter(
        played=True).order_by('started_time')

    innings2_bowling = BowlingInnings.objects.filter(match=match).filter(team=team_batting).filter(
        played=True).order_by('started_time')

    innings1_fallofwicket = Score.objects.filter(match=match).filter(innings='First').filter(wicket=True)
    innings2_fallofwicket = Score.objects.filter(match=match).filter(innings='Second').filter(wicket=True)
    context.update({'all_scores': None, 'match': match, 'batting_team': batting_team, 'bowling_team':
        bowling_team, 'innings1_batting': innings1_batting, 'innings1_bowling': innings1_bowling,
                    'innings2_batting': innings2_batting, 'innings2_bowling': innings2_bowling,
                    'innings1_fallofwicket': innings1_fallofwicket, 'innings2_fallofwicket':
                        innings2_fallofwicket, 'match_additional': match_additional, 'current_innings':
                        current_innings, 'commentary_first_innings' : commentary_first_innings,
                    'commentary_second_innings' : commentary_second_innings})
    return render(request, 'search/match_details.html',context)


def tournaments_matches(request, tournament_id):

    tournament=Tournament.objects.get(id=tournament_id)
    al_matches = tournament.match_set.all()

    try:
        P = Player.objects.get(pk=request.user.id)
        context = { 'tournament':tournament,'matches':al_matches,'P': P}
    except Exception:
        try:
            o = Organizer.objects.get(pk=request.user.id)
            context = {'tournament':tournament,'matches':al_matches, 'O': o}
        except Exception:
            context = {'tournament':tournament,'matches':al_matches, 'O': None}
    return render(request, 'search/tournament_matches.html', context)



