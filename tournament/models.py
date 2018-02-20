from django.db import models

# Create your models here.


class Tournament(models.Model):
    name = models.CharField(max_length=20, unique=True)
    place = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(default=None)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=20, unique=True)
    owner = models.CharField(max_length=20)
    logo = models.ImageField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Match(models.Model):
    tournament=models.ForeignKey(Tournament,on_delete=models.CASCADE)
    team_1=models.ForeignKey('Team',related_name='team_1',on_delete=models.DO_NOTHING)
    team_2=models.ForeignKey('Team',related_name='team_2',on_delete=models.DO_NOTHING)
    overs=models.IntegerField()
    winner=models.ForeignKey('Team',related_name='winner',on_delete=models.DO_NOTHING)

class Score(models.Model):
    match=models.ForeignKey(Match,on_delete=models.CASCADE)
    innings= [
        ('First', 'First'),
        ('Second', 'Second'),

    ]
    batting_team=models.ForeignKey('Team',related_name='batting_team',on_delete=models.DO_NOTHING)
    bowling_team = models.ForeignKey('Team', related_name='bowling_team', on_delete=models.DO_NOTHING)
    ball_number=models.IntegerField()
    over_number=models.IntegerField()
   # bowler=models.ForeignKey('Player',related_name='bowler',on_delete=models.DO_NOTHING)
    #batsman=models.ForeignKey('Player',related_name='batsman',on_delete=models.DO_NOTHING)
    run=models.IntegerField()
    extra_type=[
        ('Wide','Wide'),
        ('NoBall','NoBall'),
        ('DeadBall','DeadBall')
    ]
    extra_run=models.IntegerField()
    is_wicket=models.BooleanField(default=False)
    wicket_type=[
        ('RunOut','RunOut'),
        ('Catch','Catch'),
        ('Bowled','Bowled'),
        ('Lbw','Lbw'),
        ('Stumps','Stumps'),
        ('HitWicket','HitWicket')
    ]

