from django.db.models import Max
from django.shortcuts import render, redirect

from search.filters import PlayerFilter
from .models import Team, Tournament, Match, ScoreCard, Score
from player.models import Player
from .forms import TournamentCreationForm, TeamCreationForm, MatchCreationForm, ScoreUpdateForm, TossForm,\
    OverForm, OpenerForm1, OpenerForm2
from django.contrib import messages
from organizer.models import Organizer
from .utils import rr_schedule
from performance.models import PerformanceMatchWise, PerformanceTotal
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


def match(request, tournament_id, match_id):
    tournament = Tournament.objects.get(id=tournament_id)
    match = Match.objects.get(id=match_id)
    team1 = match.team_1
    team2 = match.team_2
    batting_team = team1
    bowling_team = team2

    if match.toss_stored:
        team = Team.objects.get(id=match.toss_winner_id)
        choice = match.toss_winner_choice
        match.toss_winner = team
        match.toss_winner_choice = choice
        if choice == 'Batting':
            if team == team1:
                batting_team = team1
                bowling_team = team2
            else:
                batting_team = team2
                bowling_team = team1
        else:
            if team == team1:
                batting_team = team2
                bowling_team = team1
            else:
                batting_team = team1
                bowling_team = team2
        match.toss_stored = True
        match.save()

    commentary_first_innings = Score.objects.filter(match=match).filter(innings='First').order_by(
        'over_number')
    commentary_second_innings = Score.objects.filter(match=match).filter(innings='Second').order_by(
        'over_number')
    toss_form = TossForm(match)
    overs_form = OverForm()
    opener_form1 = OpenerForm1(batting_team)
    opener_form2 = OpenerForm2(bowling_team)
    team1_players = PerformanceMatchWise.objects.filter(team=batting_team).filter(match=match).order_by(
           'started_time')
    team2_players = PerformanceMatchWise.objects.filter(team=bowling_team).filter(match=match).order_by(
            'started_time')
    context = {'all_scores':None,'match':match,'tournament':tournament,'batting_team':batting_team,
                   'bowling_team': bowling_team, 'toss_form': toss_form, 'overs_form': overs_form,
                    'team1_players': team1_players,'team2_players': team2_players,
               'commentary_first_innings': commentary_first_innings, 'opener_form1': opener_form1,
               'opener_form2': opener_form2, 'commentary_second_innings': commentary_second_innings}
    return render(request,'tournament/match_templates/current_match.html', context)


def match_overs(request, tournament_id, match_id):
    match = Match.objects.get(id=match_id)

    if request.method == 'POST':
        if match.overs == 0:
            form = OverForm(request.POST)
            if form.is_valid():
                overs = form.cleaned_data['overs']
                match.overs = overs
                match.save()
                return redirect('tournament:match', tournament_id, match_id)
            else:
                messages.success(request, 'Overs Information is not valid')
                return redirect('tournament:match', tournament_id, match_id)
        else:
            messages.success(request, 'Overs Information Already filled')
            return redirect('tournament:match', tournament_id, match_id)


def match_toss(request, tournament_id, match_id):
    match = Match.objects.get(id=match_id)

    if request.method == 'POST':
        if match.toss_stored == False:
            form = TossForm(match, request.POST)
            if form.is_valid():
                team = form.cleaned_data['toss_winner']
                team = Team.objects.get(id=team)
                choice = form.cleaned_data['toss_winner_choice']
                match.toss_winner = team
                match.toss_winner_choice = choice
                match.toss_stored = True
                match.save()
                return redirect('tournament:match', tournament_id, match_id)
            else:
                messages.success(request, 'Toss Information is not valid')
                return redirect('tournament:match', tournament_id, match_id)
        else:
            messages.success(request, 'Toss Information Already filled')
            return redirect('tournament:match', tournament_id, match_id)


def match_openers_innings1(request, tournament_id, match_id):
    match = Match.objects.get(id=match_id)
    team1 = match.team_1
    team2 = match.team_2
    if match.toss_winner_choice == 'Batting':
        if match.toss_winner == team1:
            batting_team = team1
        else:
            batting_team = team2
    else:
        if match.toss_winner == team1:
            batting_team = team2
        else:
            batting_team = team1

    if request.method == 'POST':
        form = OpenerForm1(batting_team, request.POST)
        if form.is_valid():
            striker_innings1 = form.cleaned_data['striker_innings1']
            match.striker_innings1 = PerformanceMatchWise.objects.filter(match=match).filter(
                player=striker_innings1).first()
            non_striker_innings1 = form.cleaned_data['non_striker_innings1']
            match.non_striker_innings1 = PerformanceMatchWise.objects.filter(match=match).filter(
                player=non_striker_innings1).first()
            match.openers_selected_innings1 = True
            match.save()
            return redirect('tournament:match', tournament_id, match_id)
        else:
            messages.success(request, 'Information is not valid')
            return redirect('tournament:match', tournament_id, match_id)
    else:
        messages.success(request, 'Information Already filled')
        return redirect('tournament:match', tournament_id, match_id)


def match_openers_innings2(request, tournament_id, match_id):
    match = Match.objects.get(id=match_id)
    team1 = match.team_1
    team2 = match.team_2
    if match.toss_winner_choice == 'Bowling':
        if match.toss_winner == team1:
            batting_team = team1

        else:
            batting_team = team2
    else:
        if match.toss_winner == team1:
            batting_team = team2
        else:
            batting_team = team1

    if request.method == 'POST':
        form = OpenerForm2(batting_team, request.POST)
        print(form)
        if form.is_valid():
            striker_innings2 = form.cleaned_data['striker_innings2']
            match.striker_innings2 = PerformanceMatchWise.objects.filter(match=match).filter(
                player=striker_innings2).first()
            non_striker_innings2 = form.cleaned_data['non_striker_innings2']
            match.non_striker_innings2 = PerformanceMatchWise.objects.filter(match=match).filter(
                player=non_striker_innings2).first()
            match.openers_selected_innings2 = True
            match.save()
            return redirect('tournament:match', tournament_id, match_id)
        else:
            messages.success(request, 'Information is not valid')
            return redirect('tournament:match', tournament_id, match_id)
    else:
        messages.success(request, 'Information Already filled')
        return redirect('tournament:match', tournament_id, match_id)


def submit_match(request, match_id):
    match = Match.objects.get(pk=match_id)
    tournament = Tournament.objects.get(pk=match.tournament.id)
    if match.match_status == 1:
        team_1 = Team.objects.get(pk=match.team_1.id)
        team_2 = Team.objects.get(pk=match.team_2.id)
        score_card = ScoreCard()
        score_card.save()
        score_card.team_1 = team_1
        score_card.team_2 = team_2
        score_card.name = team_1.name + ' vs ' + team_2.name
        score_card.match = match
        score_card.tournament = tournament
        team_1_players = PerformanceMatchWise.objects.filter(team=team_1)
        team_2_players = PerformanceMatchWise.objects.filter(team=team_2)
        for player in team_1_players:
            player.status = True
            performance = PerformanceTotal.objects.get(player=Player.objects.get(id=player.player.id))
            performance.matches += 1
            performance.save()
            player.save()
            score_card.team_1_players.add(player)
        for player in team_2_players:
            player.status = True
            performance = PerformanceTotal.objects.get(player=Player.objects.get(id=player.player.id))
            performance.matches += 1
            performance.save()
            player.save()
            score_card.team_2_players.add(player)
        score_card.save()
        match.match_status = 2
        match.save()
        messages.success(request, 'Successfully Submitted')
        return redirect('tournament:match', tournament.id, match_id)
    else:
        messages.success(request, 'Already Submitted')
        return redirect('tournament:match', tournament.id, match_id)


def submit_tournament(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    if tournament.tournament_status == 1:
        players = PerformanceMatchWise.objects.filter(tournament=tournament)
        for player in players:
            performance = PerformanceTotal.objects.get(player=Player.objects.get(id=player.player.id))
            performance.batting_runs += player.batting_runs
            performance.tournaments += 1
            performance.wickets = player.wickets
            performance.batting_balls += player.batting_balls
            performance.save()
            if performance.matches:
                performance.batting_avg = performance.batting_runs/performance.matches
            if performance.wickets:
                performance.bowling_avg = performance.bowling_runs/performance.wickets
            if performance.batting_balls:
                performance.strike_rate = (performance.batting_runs/performance.batting_balls)*100
            if player.batting_runs > performance.high_score:
                performance.high_score = player.batting_runs
            if player.batting_runs > 50:
                performance.fifties += 1
            if player.batting_runs > 100:
                performance.hundreds += 1
            performance.sixes += player.sixes
            performance.fours += player.fours
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
        Organizer.objects.get(pk=request.user.id)
        tournament = Tournament.objects.get(pk=tournament_id)
        team_1 = Team.objects.get(id=team_1_id)
        team_2 = Team.objects.get(id=team_2_id)
        match = Match()
        match.tournament = tournament
        match.team_1 = team_1
        match.team_2 = team_2
        match.winner = match.team_1
        match.overs = 0
        match.name = match
        match.save()
        team1_players = team_1.players.all()
        team2_players = team_2.players.all()
        for player in team1_players:
            performance = PerformanceMatchWise()
            performance.player = player
            performance.match = match
            performance.tournament = tournament
            performance.team = team_1
            performance.save()
        for player in team2_players:
            performance = PerformanceMatchWise()
            performance.player = player
            performance.match = match
            performance.tournament = tournament
            performance.team = team_2
            performance.save()



def enter_score(request, tournament_id, match_id, batting_team_id, bowling_team_id, innings):
    match = Match.objects.get(pk=match_id)
    tournament = Tournament.objects.get(pk=tournament_id)
    batting_team = Team.objects.get(pk=batting_team_id)
    bowling_team = Team.objects.get(pk=bowling_team_id)

    if match.match_status == 2:
        messages.success(request, 'Match already Submitted')
        return redirect('tournament:match', tournament_id, match_id)
    if match.toss_stored == True:
        if innings == 0:
            innings = 'First'
            f = 0
        else:
            innings = 'Second'
            f = 1
        if request.method == 'POST':
            form = ScoreUpdateForm(batting_team, bowling_team, match, request.POST)
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

                batsman = Player.objects.get(id=batsman)
                p = PerformanceMatchWise.objects.filter(match=match).filter(player=batsman).first()
                if p.started_time is None:
                    p.started_time = datetime.now()
                p.batting_runs += run
                p.played = True
                match.team_1_score += run
                p.team = batting_team
                if not is_extra:
                    p.batting_balls += 1
                p.strike_rate = (p.batting_runs/p.batting_balls)*100
                if six:
                    p.sixes += 1
                if four:
                    p.fours += 1
                p.status = 'batting'
                if is_wicket:
                    p.status = 'out'
                    match.team_1_wickets += 1
                p.save()

                bowler = Player.objects.get(id=bowler)
                q = PerformanceMatchWise.objects.filter(match=match).filter(player=bowler).first()
                if q.started_time is None:
                    q.started_time = datetime.now()
                q.played = True
                q.team = bowling_team
                if ball_number >= 6:
                    q.bowling_overs += 1
                q.bowling_runs += run
                if extra_run:
                    q.bowling_runs += extra_run
                if is_wicket:
                    q.wickets += 1
                    out_batsman = Player.objects.get(id=out_batsman)
                    p = PerformanceMatchWise.objects.filter(match=match).filter(player=out_batsman).first()
                    p.out = True
                    p.out_type = wicket_type
                    p.save()
                    if match.striker_innings1 == p:
                        match.striker_innings1 = PerformanceMatchWise.objects.filter(match=match).filter(
                            team=batting_team).filter(out=False).exclude(id=match.non_striker_innings1.id).first()
                        match.save()
                    elif match.non_striker_innings1 == p:
                        match.non_striker_innings1 = PerformanceMatchWise.objects.filter(match=match).filter(
                            team=batting_team).filter(out=False).exclude(id=match.striker_innings1.id).first()
                        match.save()
                    q.wickets_players.add(out_batsman)
                    p.save()
                if q.wickets:
                    q.bowling_avg = (q.bowling_runs/q.wickets)
                q.save()

                score = Score()
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
                return redirect('tournament:enter_score', tournament_id, match_id, batting_team,
                                bowling_team, f)
        else:
            form = ScoreUpdateForm(batting_team, bowling_team, match)
            context = {'form': form, 'match': match, 'batting_team': batting_team,
                       'bowling_team': bowling_team, 'innings': innings}
            return render(request, 'tournament/score_templates/enter_score.html', context)
    else:
        messages.success(request, 'Please fill toss information first')
        return redirect('tournament:match', tournament_id, match_id)


def start_match(request, match_id):
    try:
        match = Match.objects.get(id=match_id)
        team1 = match.team_1
        team2 = match.team_2
        batting_team = team1
        bowling_team = team2
        tournament = Tournament.objects.get(pk=match.tournament.id)
        match.match_status = 1
        match.save()
        form = TossForm(match)
        team1_players = PerformanceMatchWise.objects.filter(team=batting_team)
        team2_players = PerformanceMatchWise.objects.filter(team=bowling_team)
        return render(request, 'tournament/match_templates/current_match.html',
                      {'all_scores': None, 'match': match, 'tournament': tournament, 'batting_team': batting_team,
                       'bowling_team': bowling_team, 'form': form, 'team1_players': team1_players,
                       'team2_players': team2_players})
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


