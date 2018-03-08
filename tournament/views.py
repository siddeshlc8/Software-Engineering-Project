from django.db.models import Max
from django.shortcuts import render, redirect
from .models import Team, Tournament, Match
from player.models import Player
from .forms import TournamentCreationForm, TeamCreationForm,MatchCreationForm,ScoreForm,Submit_match_form,Submit_tournament_form
from django.contrib import messages
from organizer.models import Organizer
from collections import defaultdict
# Create your views here.




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
        Organizer.objects.get(pk=request.user.id)
        all_tournament = Tournament.objects.filter(organizer=request.user.id)
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
        return render(request, 'tournament/tournament_templates/current_tournament.html', context)
    except Exception:
        return redirect('login')


def team_players(request, team_id):
    try:
        o = Organizer.objects.get(pk=request.user.id)
        current_team = Team.objects.get(pk=team_id)
        current_players = current_team.player_set.all()
        available_players = Player.objects.filter(active=False).exclude(team__pk=team_id)
        context = {'current_players': current_players, 'team': current_team, 'available_players': available_players, 'O': o}
        return render(request, 'tournament/team_templates/team_players.html', context)
    except Exception:
        return redirect('login')


def team_players_add(request, team_id, player_id):
    team_ = Team.objects.get(pk=team_id)
    player_ = Player.objects.get(pk=player_id)
    player_.active = True
    player_.save()
    team_.player_set.add(player_)
    messages.success(request,'player added successfully')
    return redirect('tournament:team_players', team_id)


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
        return redirect()


def enter_score(request, tournament_id, match_id,batting_team_id,bowling_team_id):

    tournament = Tournament.objects.get(pk=tournament_id)
    batting_team=Team.objects.get(pk=batting_team_id)
    bowling_team=Team.objects.get(pk=bowling_team_id)
    if request.method == 'POST':

        form = ScoreForm(tournament, batting_team,bowling_team,request.POST)
        match = Match.objects.get(pk=match_id)
        match.match_status=1
        match.save()
        tournament.tournament_status=1
        tournament.save()
        if form.is_valid():
            score = form.save(commit=False)
            score.match = match
            score.save()
            return redirect('tournament:scores', tournament_id,match_id)
        else:
            messages.error(request, 'Please correct the error below.')
            return redirect('tournament:enter_score', tournament_id,match_id)
    else:
        match = Match.objects.get(pk=match_id)
        score=match.score_set.filter(match_id=match_id)


        target_dict = {}
        if score.exists():
            overs = score.aggregate(Max('over_number'))

            max = overs['over_number__max']
        else:
            max=0

        while max!=0:
          over_score=match.score_set.filter(over_number=max)
          target_dict[max] = {}
          for balls in  over_score:
            target_dict[max][balls.ball_number] = balls.run
          max=max-1

        form = ScoreForm(tournament, batting_team,bowling_team)
        context = {'form': form ,
                   'score':score,

                   'target_dict' :target_dict
                   }
        return render(request, 'tournament/score_templates/enter_score.html', context)


def  scores(request, tournament_id,match_id):
    match=Match.objects.get(id=match_id)
    team1=match.team_1
    team2=match.team_2
    players_team1=team1.player_set.all()
    players_team2=team2.player_set.all()
    all_scores =match.score_set.all()
    return render(request,'tournament/score_templates/scores.html',{'all_scores':all_scores,'match':match,'tournament_id':tournament_id,'players_team1':players_team1,'players_team2':players_team2 ,'team1':team1,'team2':team2})

def  match(request, tournament_id,match_id):
    match=Match.objects.get(id=match_id)
    tournament=Tournament.objects.get(id=tournament_id)
    return render(request,'tournament/match_templates/current_match.html',{'tournament':tournament,'match':match})

def  submit_match(request, tournament_id,match_id):
    current_tournament = Tournament.objects.get(pk=tournament_id)
    match = Match.objects.get(pk=match_id)
    if request.method == 'POST':
        form=Submit_match_form(request.POST)
        team1=match.team_1
        team2=match.team_2

        if form['team1'].value()==team1.name and  form['team2'].value()==team2.name :
            match.match_status=2
            match.save()
            messages.success(request, 'match  sucessfully submitted')
            return redirect('tournament:match', tournament_id,match_id)
        else:
            messages.error(request, 'Please correct the error below.')
            return redirect('tournament:submit_match', tournament_id,match_id)
    else:
        form=Submit_match_form()
        return render(request, 'tournament/match_templates/submit_match.html',{'form' :form,'tournament':current_tournament,'match':match})




def submit_tournament(request, tournament_id):
    current_tournament = Tournament.objects.get(pk=tournament_id)
    if request.method == 'POST':
        form = Submit_tournament_form(request.POST)

        if form['tournament_name'].value() == current_tournament.name :
            current_tournament.tournament_status = 2
            current_tournament.save()
            messages.success(request,'tournament sucessfully submitted')
            return redirect('tournament:current_tournament', tournament_id)
        else:
            messages.error(request, 'Please correct the error below.')
            return redirect('tournament:submit_tournament', tournament_id)
    else:
        form = Submit_tournament_form()
        return render(request, 'tournament/tournament_templates/submit_tournament.html',
                      {'form': form, 'tournament': current_tournament})

