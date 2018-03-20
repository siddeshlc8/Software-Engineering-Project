from django.db.models import Max
from django.shortcuts import render, redirect
from search.filters import PlayerFilter
from .models import Team, Tournament, Match, ScoreCard, Score, FirstInnings, SecondInnings, MatchAdditional
from player.models import Player
from .forms import TournamentCreationForm, TeamCreationForm, MatchCreationForm, ScoreUpdateForm, TossForm,\
    OverForm, OpenerForm1, OpenerForm2, SelectBatsmanForm, OpenerForm
from django.contrib import messages
from organizer.models import Organizer
from .utils import rr_schedule
from performance.models import PerformanceTotal, PerformanceMatch, BattingInnings, \
    BowlingInnings
import itertools
from datetime import datetime


def create_tournament(request):
    try:
        organizer = Organizer.objects.get(pk=request.user.id)
        if request.method == 'POST':
            form = TournamentCreationForm(request.POST)
            if form.is_valid():
                new_tournament = form.save(commit=False)
                new_tournament.organizer = organizer
                new_tournament.save()
                messages.success(request,'tournament sucessfully created')
                return redirect('tournament:tournament')
            else:
                messages.warning(request,'give proper information')
                return render(request, 'tournament/tournament_templates/create_tournament.html', {'form':form})
        else:
            form = TournamentCreationForm()
            context = {'form': form}
            return render(request, 'tournament/tournament_templates/create_tournament.html', context)
    except Exception:
        return redirect('login')


def create_team(request, tournament_id):
    try:
        Organizer.objects.get(pk=request.user.id)
        if request.method == 'POST':
            form = TeamCreationForm(request.POST)
            current_tournament = Tournament.objects.get(pk=tournament_id)
            if form.is_valid():
                team = form.save(commit=False)
                team.tournament = current_tournament
                team.save()
                messages.success(request,'team sucessfully created')
                return redirect('tournament:current_tournament', tournament_id)
            else:
                messages.error(request, 'Please provide proper details')
                return redirect('tournament:current_tournament',  tournament_id)
        else:
            form = TeamCreationForm()
            context = {'form': form}
            return render(request, 'tournament/tournament_templates/create_tournament.html', context)
    except Exception:
               return redirect('login')


def tournament(request):
    try:
        o=Organizer.objects.get(pk=request.user.id)
        all_tournament = Tournament.objects.filter(organizer=o)
        context = {'all_tournament': all_tournament}
        return render(request, 'tournament/tournament_templates/tournaments.html', context)
    except Exception:
        return redirect('login')


def current_tournament(request, tournament_id):
    try:
        Organizer.objects.get(pk=request.user.id)
        current_tournament = Tournament.objects.get(pk=tournament_id)
        teams = current_tournament.team_set.all()
        context = {'current_tournament': current_tournament, 'teams': teams}
        return render(request, 'tournament/tournament_templates/current_tournaments.html', context)
    except Exception:
        return redirect('login')


def team_players(request, team_id):
    try:
        o = Organizer.objects.get(pk=request.user.id)
        current_team = Team.objects.get(pk=team_id)
        current_players = current_team.players.all()
        available_players = Player.objects.filter(active=False)
        context = {'current_players': current_players, 'team': current_team, 'available_players': available_players, 'O': o}
        return render(request, 'tournament/team_templates/team_players.html', context)
    except Exception:
        return redirect('login')


def team_players_add(request, team_id, player_id):
        team_ = Team.objects.get(pk=team_id)
        player_ = Player.objects.get(pk=player_id)
        player_.active = True
        player_.save()
        team_.players.add(player_)
        messages.success(request,'player' + player_.get_full_name() + ' added successfully')
        return redirect('tournament:add_players', team_id)


def add_players(request, team_id):
     team_ = Team.objects.get(pk=team_id)
     players = Player.objects.all().filter(active=False)
     players_filter = PlayerFilter(request.GET, queryset=players)
     try:
         player = Player.objects.get(pk=request.user.id)
         context = {'players': players, 'P': player, 'filter': players_filter}
     except Exception:
         try:
             o = Organizer.objects.get(pk=request.user.id)
             context = {'players': players, 'O': o, 'filter': players_filter,'team':team_}
         except Exception:
             return redirect('login')
     return render(request,'tournament/team_templates/add_players.html',context)


def all_matches(request, tournament_id):
    tournament=Tournament.objects.get(id=tournament_id)
    al_matches = tournament.match_set.all()
    return render(request,'tournament/match_templates/matches.html',{'tournament':tournament,'matches':al_matches})


def create_match(request, tournament_id):
    try:
        Organizer.objects.get(pk=request.user.id)
        tournament = Tournament.objects.get(pk=tournament_id)
        if request.method == 'POST':
            form = MatchCreationForm(tournament, request.POST)
            if form.is_valid():
                match = form.save(commit=False)
                match.tournament = tournament
                match.winner=match.team_1
                match.save()
                messages.success(request,'created match sucessfully')
                return redirect('tournament:all_matches', tournament_id)
            else:
                messages.error(request, 'Please correct the error below.')
                return redirect('tournament:create_match', tournament_id)
        else:
            form = MatchCreationForm(tournament)
            context = {'form': form}
            return render(request, 'tournament/match_templates/create_match.html', context)
    except Exception:
        return redirect('login')


def create_schedule(request, tournament_id):
    try:
        o = Organizer.objects.get(id=request.user.id)
        tournament = Tournament.objects.get(pk=tournament_id)
        if tournament.tournament_schedule == 0:
            teams = Team.objects.filter(tournament=Tournament.objects.get(id=tournament_id))
            n = teams.__len__()
            if n%2 !=0 :
                messages.success(request, 'No of teams should be even')
                return redirect('tournament:all_matches', tournament_id)
            result = rr_schedule(n/2)
            for i in result:
                for j in i:
                    #print(i)
                    team_1 = teams[j[0]-1]
                    team_2 = teams[j[1]-1]
                    create_match1(request, tournament_id, team_1.id, team_2.id)
            tournament.tournament_schedule = 1
            tournament.save()
            messages.success(request, 'Schedule successfully created')
            return redirect('tournament:all_matches', tournament_id)
        else:
            messages.success(request, 'Schedule Already created')
            return redirect('tournament:all_matches', tournament_id)
    except Exception:
        return redirect('login')


def create_match1(request, tournament_id, team_1_id, team_2_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    team_1 = Team.objects.get(id=team_1_id)
    team_2 = Team.objects.get(id=team_2_id)

    match = Match()
    match.tournament = tournament
    match.team_1 = team_1
    match.team_2 = team_2
    match.name = match
    match.save()

    first_innings = FirstInnings()
    first_innings.save()
    second_innings = SecondInnings()
    second_innings.save()
    match_additional = MatchAdditional()
    match_additional.current_innings = 'First'
    match_additional.save()
    match.first_innings = first_innings
    match.second_innings = second_innings
    match.match_additional = match_additional
    match.save()

    team1_players = team_1.players.all()
    team2_players = team_2.players.all()
    for player in team1_players:
        performance = PerformanceMatch()
        performance.player = player
        performance.match = match
        performance.tournament = tournament
        performance.team = team_1
        performance.played = True
        batting_innings = BattingInnings()
        batting_innings.save()
        bowling_innings = BowlingInnings()
        bowling_innings.save()
        performance.batting_innings = batting_innings
        performance.bowling_innings = bowling_innings
        performance.save()
    for player in team2_players:
        performance = PerformanceMatch()
        performance.player = player
        performance.match = match
        performance.tournament = tournament
        performance.team = team_2
        performance.played = True
        batting_innings = BattingInnings()
        batting_innings.save()
        bowling_innings = BowlingInnings()
        bowling_innings.save()
        performance.batting_innings = batting_innings
        performance.bowling_innings = bowling_innings
        performance.save()


def match(request, match_id):
    match = Match.objects.get(id=match_id)
    innings = match.match_additional.current_innings

    if innings == 'First':
        current_innings = match.first_innings
        bowling_team = match.first_innings.bowling_team
        batting_team = match.first_innings.batting_team
    else:
        current_innings = match.second_innings
        bowling_team = match.second_innings.bowling_team
        batting_team = match.second_innings.batting_team

    if match.match_additional.toss_stored:

        commentary_first_innings = Score.objects.filter(match=match).filter(innings=innings).order_by(
            'over_number')
        commentary_second_innings = Score.objects.filter(match=match).filter(innings=innings).order_by(
            'over_number')
        toss_form = TossForm(match)
        overs_form = OverForm()
        opener_form = OpenerForm(batting_team)

        innings1_batting = PerformanceMatch.objects.filter(team=match.first_innings.batting_team).filter(match=match).filter(
            batting_innings__played=True).filter(batting_innings__played=True).order_by(
            'batting_innings__started_time')
        innings1_bowling = PerformanceMatch.objects.filter(team=match.first_innings.bowling_team).filter(match=match).filter(
            bowling_innings__played=True).filter(bowling_innings__played=True).order_by(
            'bowling_innings__started_time')
        innings2_batting = PerformanceMatch.objects.filter(team=match.second_innings.batting_team).filter(match=match).filter(
            batting_innings__played=True).filter(batting_innings__played=True).order_by(
            'batting_innings__started_time')
        innings2_bowling = PerformanceMatch.objects.filter(team=match.second_innings.bowling_team).filter(match=match).filter(
            bowling_innings__played=True).filter(bowling_innings__played=True).order_by(
            'bowling_innings__started_time')

        innings1_fallofwicket = Score.objects.filter(match=match).filter(innings='First').filter(wicket=True)
        innings2_fallofwicket = Score.objects.filter(match=match).filter(innings='Second').filter(wicket=True)

        context = {'all_scores': None, 'match': match, 'tournament': tournament, 'batting_team': batting_team,
                   'bowling_team': bowling_team, 'toss_form': toss_form, 'overs_form': overs_form,
                   'innings1_batting': innings1_batting, 'innings1_bowling': innings1_bowling,
                   'innings2_batting': innings2_batting, 'innings2_bowling': innings2_bowling,
                   'commentary_first_innings': commentary_first_innings, 'opener_form': opener_form,
                   'commentary_second_innings': commentary_second_innings,
                   'innings1_fallofwicket': innings1_fallofwicket, 'innings2_fallofwicket': innings2_fallofwicket}
        return render(request, 'tournament/match_templates/current_match.html', context)
    else:
        toss_form = TossForm(match)
        overs_form = OverForm()
        context = {'all_scores': None, 'match': match, 'tournament': tournament, 'batting_team': None,
                   'bowling_team': None, 'toss_form': toss_form, 'overs_form': overs_form,
                   'innings1_batting': None, 'innings1_bowling': None,
                   'innings2_batting': None, 'innings2_bowling': None,
                   'commentary_first_innings': None, 'opener_form': None,
                   'commentary_second_innings': None,
                   'innings1_fallofwicket': None, 'innings2_fallofwicket': None}
        return render(request, 'tournament/match_templates/current_match.html', context)


def match_overs(request, match_id):
    match = Match.objects.get(id=match_id)

    if request.method == 'POST':
        if match.overs == 0:
            form = OverForm(request.POST)
            if form.is_valid():
                overs = form.cleaned_data['overs']
                match.overs = overs
                match.save()
                return redirect('tournament:match', match_id)
            else:
                messages.success(request, 'Overs Information is not valid')
                return redirect('tournament:match', match_id)
        else:
            messages.success(request, 'Overs Information Already filled')
            return redirect('tournament:match', match_id)


def match_toss(request, match_id):
    match = Match.objects.get(id=match_id)

    if request.method == 'POST':
        if match.match_additional.toss_stored is False:
            form = TossForm(match, request.POST)
            if form.is_valid():

                team = form.cleaned_data['toss_winner']
                team = Team.objects.get(id=team)
                choice = form.cleaned_data['toss_winner_choice']
                match.toss_winner = team
                match.toss_winner_choice = choice
                match.save()

                if match.toss_winner_choice == 'Batting':
                    if match.toss_winner == match.team_1:
                        match.first_innings.batting_team = match.team_1
                        match.first_innings.bowling_team = match.team_2
                        match.second_innings.batting_team = match.team_2
                        match.second_innings.bowling_team = match.team_1
                    else:
                        match.first_innings.batting_team = match.team_2
                        match.first_innings.bowling_team = match.team_1
                        match.second_innings.batting_team = match.team_1
                        match.second_innings.bowling_team = match.team_2
                else:
                    if match.toss_winner == match.team_1:
                        match.first_innings.batting_team = match.team_2
                        match.first_innings.bowling_team = match.team_1
                        match.second_innings.batting_team = match.team_1
                        match.second_innings.bowling_team = match.team_2
                    else:
                        match.first_innings.batting_team = match.team_1
                        match.first_innings.bowling_team = match.team_2
                        match.second_innings.batting_team = match.team_2
                        match.second_innings.bowling_team = match.team_1

                match.first_innings.save()
                match.second_innings.save()

                match.match_additional.toss_stored = True
                match.match_additional.save()

                return redirect('tournament:match', match_id)
            else:
                messages.success(request, 'Toss Information is not valid')
                return redirect('tournament:match', match_id)
        else:
            messages.success(request, 'Toss Information Already filled')
            return redirect('tournament:match', match_id)


def match_openers(request, match_id):
    match = Match.objects.get(id=match_id)
    innings = match.match_additional.current_innings

    if innings == 'First':
        current_innings = match.first_innings
    else:
        current_innings = match.second_innings

    if request.method == 'POST':
        form = OpenerForm(current_innings.batting_team, request.POST)
        if form.is_valid():

            striker = form.cleaned_data['striker']
            current_innings.striker = PerformanceMatch.objects.filter(match=match).filter(
                player=striker).first()
            current_innings.striker.batting_innings.status = 'batting'
            current_innings.striker.batting_innings.played = True
            current_innings.striker.batting_innings.started_time = datetime.now()
            current_innings.striker.batting_innings.save()
            current_innings.save()

            non_striker = form.cleaned_data['non_striker']
            current_innings.non_striker = PerformanceMatch.objects.filter(match=match).filter(
                player=non_striker).first()
            current_innings.non_striker.batting_innings.status = 'batting'
            current_innings.non_striker.batting_innings.played = True
            current_innings.non_striker.batting_innings.started_time = datetime.now()
            current_innings.non_striker.batting_innings.save()
            current_innings.save()

            current_innings.openers_selected = True
            current_innings.save()

            return redirect('tournament:match', match_id)
        else:
            messages.success(request, 'Information is not valid')
            return redirect('tournament:match', match_id)
    else:
        messages.success(request, 'Information Already filled')
        return redirect('tournament:match', match_id)


def submit_match(request, match_id):
    match = Match.objects.get(pk=match_id)
    tournament = Tournament.objects.get(pk=match.tournament.id)
    if match.match_status == 1:
        team_1 = Team.objects.get(pk=match.team_1.id)
        team_2 = Team.objects.get(pk=match.team_2.id)

        team_1_players = PerformanceMatch.objects.filter(team=team_1)
        team_2_players = PerformanceMatch.objects.filter(team=team_2)
        for player in team_1_players:
            player.status = True
            performance = PerformanceTotal.objects.get(player=Player.objects.get(id=player.player.id))
            performance.matches += 1
            performance.save()
            if player.batting_innings.played:
                performance.batting_innings += 1
            if player.bowling_innings.played:
                performance.bowling_innings += 1
            if player.batting_innings.status == 'batting':
                player.batting_innings.status = 'not out'
                player.batting_innings.save()
            elif player.batting_innings.status is None:
                player.batting_innings.status = 'not played'
                player.batting_innings.save()
            player.save()
        for player in team_2_players:
            player.status = True
            performance = PerformanceTotal.objects.get(player=Player.objects.get(id=player.player.id))
            performance.matches += 1
            performance.save()
            if player.batting_innings.played:
                performance.batting_innings += 1
            if player.bowling_innings.played:
                performance.bowling_innings += 1
            if player.batting_innings.status == 'batting':
                player.batting_innings.status = 'not out'
                player.batting_innings.save()
            elif player.batting_innings.status is None:
                player.batting_innings.status = 'not played'
                player.batting_innings.save()
            player.save()

        match.match_status = 2
        match.save()
        messages.success(request, 'Successfully Submitted')
        return redirect('tournament:match', match_id)
    else:
        messages.success(request, 'Already Submitted')
        return redirect('tournament:match', match_id)


def submit_tournament(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    if tournament.tournament_status == 1:
        players = PerformanceMatch.objects.filter(tournament=tournament)
        for player in players:
            performance = PerformanceTotal.objects.get(player=Player.objects.get(id=player.player.id))
            performance.batting_runs += player.batting_innings.batting_runs
            performance.tournaments += 1
            performance.wickets = player.bowling_innings.wickets
            performance.batting_balls += player.batting_innings.batting_balls
            performance.save()
            if performance.matches:
                performance.batting_avg = performance.batting_runs/performance.matches
            if performance.wickets:
                performance.bowling_avg = performance.bowling_runs/performance.wickets
            if performance.batting_balls:
                performance.strike_rate = (performance.batting_runs/performance.batting_balls)*100
            if player.batting_innings.batting_runs > performance.high_score:
                performance.high_score = player.batting_innings.batting_runs
            if player.batting_innings.batting_runs > 50:
                performance.fifties += 1
            if player.batting_innings.batting_runs > 100:
                performance.hundreds += 1
            performance.sixes += player.batting_innings.sixes
            performance.fours += player.batting_innings.fours
            performance.save()
            player.player.active = False
            player.player.save()
        tournament.tournament_status = 2
        tournament.save()
        messages.success(request, 'Successfully Submitted')
        return redirect('tournament:current_tournament', tournament.id)
    else:
        messages.success(request, 'Already Submitted')
        return redirect('tournament:current_tournament', tournament.id)


def tournament_info_edit(request,tournament_id):
    try:
        Organizer.objects.get(pk=request.user.id)
        tournament = Tournament.objects.get(pk=tournament_id)
        if request.method == 'POST':
            form = TournamentCreationForm(request.POST, instance=tournament)
            if form.is_valid():
                form.save()
                messages.success(request,'successfully edited information !')
                return redirect('tournament:current_tournament',tournament_id)
        else:
            form = TournamentCreationForm(instance=tournament)
            context = {'form': form }
            return render(request, 'tournament/tournament_templates/tournament_details_edit.html', context)
    except Exception:
        return redirect('login')


def submit_innings(request, match_id):
    match = Match.objects.get(pk=match_id)
    innings = match.match_additional.current_innings

    if innings == 'First':
        match.match_additional.current_innings = 'Second'
        match.match_additional.save()
    else:
        match.match_additional.current_innings = 'Over'
        match.match_additional.save()

    return redirect('tournament:match', match_id)


def enter_score(request, match_id):
    match = Match.objects.get(pk=match_id)
    innings = match.match_additional.current_innings

    if innings == 'First':
        current_innings = match.first_innings
        bowling_team = match.first_innings.bowling_team
        batting_team = match.first_innings.batting_team
    else:
        current_innings = match.second_innings
        bowling_team = match.second_innings.bowling_team
        batting_team = match.second_innings.batting_team

    if match.match_status == 2:
        messages.success(request, 'Match already Submitted')
        return redirect('tournament:match', match_id)

    if match.match_additional.toss_stored is True:
        player1 = current_innings.striker
        player2 = current_innings.non_striker

        if request.method == 'POST':
            form = ScoreUpdateForm(player1, player2, bowling_team, match, request.POST)
            if form.is_valid():
                ball_number = form.cleaned_data['ball_number']
                over_number = form.cleaned_data['over_number']
                bowler = form.cleaned_data['bowler']
                batsman = form.cleaned_data['batsman']
                run = form.cleaned_data['run']
                extra_type = form.cleaned_data['extra_type']
                extra_run = form.cleaned_data['extra_run']
                is_wicket = form.cleaned_data['is_wicket']
                is_extra = form.cleaned_data['is_extra']
                wicket_type = form.cleaned_data['wicket_type']
                commentary = form.cleaned_data['commentary']
                four = form.cleaned_data['four']
                six = form.cleaned_data['six']
                out_batsman = form.cleaned_data['out_batsman']

                score = Score()
                score.save()

                batsman = Player.objects.get(id=batsman)
                p = PerformanceMatch.objects.filter(match=match).filter(player=batsman).first()
                p = p.batting_innings
                p.batting_runs += run
                p.batting_innings.played = True
                p.team = batting_team
                if not is_extra:
                    p.batting_balls += 1
                p.strike_rate = (p.batting_runs / p.batting_balls) * 100
                if six:
                    p.sixes += 1
                    score.six = True
                    score.save()
                if four:
                    p.fours += 1
                    score.four = True
                    score.save()
                p.save()

                bowler = Player.objects.get(id=bowler)
                q = PerformanceMatch.objects.filter(match=match).filter(player=bowler).first()
                q = q.bowling_innings
                if q.started_time is None:
                    q.started_time = datetime.now()
                q.played = True
                q.save()
                q.team = bowling_team
                if ball_number >= 6:
                    q.bowling_overs += 1
                    over_number += 1
                    q.save()
                q.bowling_runs += run
                current_innings.current_over = over_number
                current_innings.save()
                if extra_run:
                    q.bowling_runs += extra_run
                if is_wicket:
                    q.wickets += 1
                    out_batsman = Player.objects.get(id=out_batsman)
                    p = PerformanceMatch.objects.filter(match=match).filter(player=out_batsman).first()
                    p.batting_innings.out = True
                    p.batting_innings.out_type = wicket_type
                    p.batting_innings.save()
                    p.batting_innings.status = 'out'
                    p.batting_innings.save()
                    p.save()
                    score.wicket = True
                    score.out_batsman = out_batsman
                    score.save()

                    if current_innings.striker == p:
                        current_innings.striker = None
                        current_innings.save()
                    elif current_innings.non_striker == p:
                        current_innings.non_striker = None
                        current_innings.save()

                    q.wickets_players.add(out_batsman)
                    p.save()
                if q.wickets:
                    q.bowling_avg = (q.bowling_runs / q.wickets)
                q.save()

                score.match = match
                score.innings = innings
                score.over_number = over_number
                score.ball_number = ball_number
                score.batsman = batsman
                score.bowler = bowler
                score.description = commentary
                score.batting_team = batting_team
                score.bowling_team = bowling_team
                score.save()
                return redirect('tournament:enter_score', match_id)
        else:
            if current_innings.striker is None and current_innings.non_striker is None:
                messages.success(request, 'All-Out  ')
                return redirect('tournament:match', match_id)

            bowling_team_players = PerformanceMatch.objects.filter(team=bowling_team).filter(
                match=match).filter(bowling_innings__played=True).order_by('-batting_innings__started_time')

            player = None
            if current_innings.striker is None:
                player = current_innings.non_striker.id
            elif current_innings.non_striker is None:
                player = current_innings.striker.id

            players = PerformanceMatch.objects.filter(match=match).filter(team=batting_team).filter(
                        batting_innings__out=False).exclude(id=player)

            select_new_batsman_form = SelectBatsmanForm(players)

            form = ScoreUpdateForm(player1, player2, bowling_team, match,
                                   initial={'over_number': current_innings.current_over})
            recent = Score.objects.filter(match=match).filter(innings=innings).order_by(
                'over_number')
            recent = recent[:5]
            context = {'form': form, 'match': match, 'batting_team': batting_team, 'bowling_team': bowling_team,
                       'bowling_team_players': bowling_team_players, 'player1': player1, 'player2': player2,
                       'select_new_batsman_form': select_new_batsman_form, 'players': players, 'recent': recent}
            return render(request, 'tournament/score_templates/enter_score.html', context)
    else:
        messages.success(request, 'Please fill toss information first')
        return redirect('tournament:match', match_id)


def live_scores(request, match_id):
    match = Match.objects.get(pk=match_id)
    if match.match_status == 1:
        innings = match.match_additional.current_innings

        if innings == 'First':
            current_innings = match.first_innings
            bowling_team = match.first_innings.bowling_team
            batting_team = match.first_innings.batting_team
        else:
            current_innings = match.second_innings
            bowling_team = match.second_innings.bowling_team
            batting_team = match.second_innings.batting_team

        player1 = current_innings.striker
        player2 = current_innings.non_striker

        bowling_team_players = PerformanceMatch.objects.filter(team=bowling_team).filter(
            match=match).filter(bowling_innings__played=True).order_by('-batting_innings__started_time')

        recent = Score.objects.filter(match=match).filter(innings=innings).order_by(
            'over_number')
        recent = recent[:5]
        context = {'match': match, 'batting_team': batting_team, 'bowling_team': bowling_team, 'player1': player1,
                   'player2': player2, 'recent': recent, 'bowling_team_players': bowling_team_players}
        return render(request, 'tournament/score_templates/live_score.html', context)


def select_new_batsman(request, match_id):
    match = Match.objects.get(pk=match_id)
    innings = match.match_additional.current_innings

    if innings == 'First':
        current_innings = match.first_innings
        bowling_team = match.first_innings.bowling_team
        batting_team = match.first_innings.batting_team
    else:
        current_innings = match.second_innings
        bowling_team = match.second_innings.bowling_team
        batting_team = match.second_innings.batting_team

    player = None
    if current_innings.striker is None:
        player = current_innings.non_striker.id
    elif current_innings.non_striker is None:
        player = current_innings.striker.id
    players = PerformanceMatch.objects.filter(match=match).filter(team=batting_team).filter(
        batting_innings__out=False).exclude(id=player)

    form = SelectBatsmanForm(players, request.POST)
    if form.is_valid():
        new_player = form.cleaned_data['player']
        new_player = PerformanceMatch.objects.filter(match=match).filter(player=new_player).first()
        new_player.batting_innings.played = True
        new_player.batting_innings.status = 'batting'
        new_player.batting_innings.started_time = datetime.now()
        new_player.batting_innings.save()

        if current_innings.striker is None:
            current_innings.striker = new_player
            current_innings.save()
        elif current_innings.non_striker is None:
            current_innings.non_striker = new_player
            current_innings.save()
        return redirect('tournament:enter_score', match_id)
    else:
        messages.success(request, 'Information is not valid')
        return redirect('tournament:enter_score', match_id)


def start_match(request, match_id):
    try:
        match = Match.objects.get(id=match_id)
        match.match_status = 1
        match.save()
        return redirect('tournament:match', match_id)
    except Exception:
        return redirect('login')


def start_tournament(request, tournament_id):
    try:
        o = Organizer.objects.get(id=request.user.id)
        current_tournament = Tournament.objects.get(pk=tournament_id)
        teams = current_tournament.team_set.all()
        current_tournament.tournament_status = 1
        current_tournament.save()
        context = {'current_tournament': current_tournament, 'teams': teams}
        return render(request, 'tournament/tournament_templates/current_tournaments.html', context)
    except Exception:
        return redirect('login')


