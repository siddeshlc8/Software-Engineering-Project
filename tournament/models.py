from django.db import models
from organizer.models import Organizer
from player.models import Player
from performance.models import PerformanceMatchWise


# Create your models here.


class Tournament(models.Model):
    name = models.CharField(max_length=20, unique=True)
    place = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(default=None)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    tournament_status = models.IntegerField(default=0)
    tournament_schedule = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=20, unique=True)
    owner = models.CharField(max_length=20)
    logo = models.ImageField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player)

    def __str__(self):
        return self.name


class Match(models.Model):
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    team_1 = models.ForeignKey('Team', related_name='team_1',on_delete=models.DO_NOTHING)
    team_2 = models.ForeignKey('Team', related_name='team_2',on_delete=models.DO_NOTHING)
    overs = models.IntegerField()
    match_status = models.IntegerField(default=0)
    winner = models.ForeignKey('Team', related_name='winner',on_delete=models.DO_NOTHING)
    toss_winner = models.ForeignKey('Team', related_name='toss_winner', on_delete=models.DO_NOTHING, blank=True, null=True)
    toss_winner_choice = models.CharField(max_length=10, default='Select')
    toss_stored = models.BooleanField(default=False)

    def __str__(self):
        return '  ' + self.team_1.name + '  vs  ' + self.team_2.name


class Score(models.Model):
    match=models.ForeignKey(Match, on_delete=models.CASCADE)
    innings_choice= [
        ('First', 'First'),
        ('Second', 'Second'),

    ]
    innings = models.CharField(max_length=11,choices=innings_choice)
    batting_team = models.ForeignKey('Team', related_name='batting_team', on_delete=models.DO_NOTHING)
    bowling_team = models.ForeignKey('Team', related_name='bowling_team', on_delete=models.DO_NOTHING)
    ball_number = models.IntegerField()
    over_number = models.IntegerField()
    bowler = models.ForeignKey('player.Player',related_name='bowler',null=True , on_delete=models.DO_NOTHING)
    batsman=models.ForeignKey('player.Player', related_name='batsman',null=True ,on_delete=models.DO_NOTHING)
    run=models.IntegerField()
    extra_type_choice =[
        ('Wide', 'Wide'),
        ('NoBall', 'NoBall'),
        ('DeadBall', 'DeadBall')
    ]
    extra_type = models.CharField(max_length=11, choices=extra_type_choice,null=True,blank=True)
    extra_run = models.IntegerField(default=0)
    is_wicket = models.BooleanField(default=False)

    wicket_type_choice = [
        ('RunOut', 'RunOut'),
        ('Catch', 'Catch'),
        ('Bowled', 'Bowled'),
        ('Lbw', 'Lbw'),
        ('Stumps', 'Stumps'),
        ('HitWicket', 'HitWicket')
    ]
    wicket_type = models.CharField(max_length=11, choices=wicket_type_choice, null=True, blank=True)

    def __str__(self):
        return '  ball =>  '+ str(self.ball_number) + '  runs => ' + str(self.run)


class ScoreCard(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=True, null=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, blank=True)
    team_1 = models.ForeignKey(Team, related_name='team1', on_delete=models.DO_NOTHING, null=True, blank=True)
    team_2 = models.ForeignKey(Team, related_name='team2', on_delete=models.DO_NOTHING, null=True, blank=True)
    team_1_players = models.ManyToManyField(PerformanceMatchWise, related_name='team_1_players')
    team_2_players = models.ManyToManyField(PerformanceMatchWise, related_name='team_2_players')









