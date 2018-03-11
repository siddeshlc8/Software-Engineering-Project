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
    player1 = models.ForeignKey(Player, related_name='player1', on_delete=models.DO_NOTHING, null=True)
    player2 = models.ForeignKey(Player, related_name='player2', on_delete=models.DO_NOTHING, null=True)
    player3 = models.ForeignKey(Player, related_name='player3', on_delete=models.DO_NOTHING, null=True)
    player4 = models.ForeignKey(Player, related_name='player4', on_delete=models.DO_NOTHING, null=True)
    player5 = models.ForeignKey(Player, related_name='player5', on_delete=models.DO_NOTHING, null=True)
    player6 = models.ForeignKey(Player, related_name='player6', on_delete=models.DO_NOTHING, null=True)
    player7 = models.ForeignKey(Player, related_name='player7', on_delete=models.DO_NOTHING, null=True)
    player8 = models.ForeignKey(Player, related_name='player8', on_delete=models.DO_NOTHING, null=True)
    player9 = models.ForeignKey(Player, related_name='player9', on_delete=models.DO_NOTHING, null=True)
    player10 = models.ForeignKey(Player, related_name='player10', on_delete=models.DO_NOTHING, null=True)
    player11 = models.ForeignKey(Player, related_name='player11', on_delete=models.DO_NOTHING, null=True)

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
    name = models.CharField(max_length=20, unique=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team_1 = models.ForeignKey(Team, related_name='team1', on_delete=models.DO_NOTHING)
    team_2 = models.ForeignKey(Team, related_name='team2', on_delete=models.DO_NOTHING)
    team_1_player1 = models.ForeignKey(PerformanceMatchWise, related_name='team_1_player1', on_delete=models.DO_NOTHING)
    team_1_player2 = models.ForeignKey(PerformanceMatchWise, related_name='team_1_player2', on_delete=models.DO_NOTHING)
    team_1_player3 = models.ForeignKey(PerformanceMatchWise, related_name='team_1_player3', on_delete=models.DO_NOTHING)
    team_1_player4 = models.ForeignKey(PerformanceMatchWise, related_name='team_1_player4', on_delete=models.DO_NOTHING)
    team_1_player5 = models.ForeignKey(PerformanceMatchWise, related_name='team_1_player5', on_delete=models.DO_NOTHING)
    team_1_player6 = models.ForeignKey(PerformanceMatchWise, related_name='team_1_player6', on_delete=models.DO_NOTHING)
    team_1_player7 = models.ForeignKey(PerformanceMatchWise, related_name='team_1_player7', on_delete=models.DO_NOTHING)
    team_1_player8 = models.ForeignKey(PerformanceMatchWise, related_name='team_1_player8', on_delete=models.DO_NOTHING)
    team_1_player9 = models.ForeignKey(PerformanceMatchWise, related_name='team_1_player9', on_delete=models.DO_NOTHING)
    team_1_player10 = models.ForeignKey(PerformanceMatchWise, related_name='team_1_player10',
                                        on_delete=models.DO_NOTHING)
    team_1_player11 = models.ForeignKey(PerformanceMatchWise, related_name='team_1_player11',
                                        on_delete=models.DO_NOTHING)
    team_2_player1 = models.ForeignKey(PerformanceMatchWise, related_name='team_2_player1', on_delete=models.DO_NOTHING)
    team_2_player2 = models.ForeignKey(PerformanceMatchWise, related_name='team_2_player2', on_delete=models.DO_NOTHING)
    team_2_player3 = models.ForeignKey(PerformanceMatchWise, related_name='team_2_player3', on_delete=models.DO_NOTHING)
    team_2_player4 = models.ForeignKey(PerformanceMatchWise, related_name='team_2_player4', on_delete=models.DO_NOTHING)
    team_2_player5 = models.ForeignKey(PerformanceMatchWise, related_name='team_2_player5', on_delete=models.DO_NOTHING)
    team_2_player6 = models.ForeignKey(PerformanceMatchWise, related_name='team_2_player6', on_delete=models.DO_NOTHING)
    team_2_player7 = models.ForeignKey(PerformanceMatchWise, related_name='team_2_player7', on_delete=models.DO_NOTHING)
    team_2_player8 = models.ForeignKey(PerformanceMatchWise, related_name='team_2_player8', on_delete=models.DO_NOTHING)
    team_2_player9 = models.ForeignKey(PerformanceMatchWise, related_name='team_2_player9', on_delete=models.DO_NOTHING)
    team_2_player10 = models.ForeignKey(PerformanceMatchWise, related_name='team_2_player10',
                                        on_delete=models.DO_NOTHING)
    team_2_player11 = models.ForeignKey(PerformanceMatchWise, related_name='team_2_player11',
                                        on_delete=models.DO_NOTHING)









