from django.db import models
from player.models import Player


class PerformanceTotal(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    tournaments = models.BigIntegerField(default=0)
    matches = models.BigIntegerField(default=0)
    batting_innings = models.BigIntegerField(default=0)
    batting_runs = models.BigIntegerField(default=0)
    batting_balls = models.BigIntegerField(default=0)
    high_score = models.BigIntegerField(default=0)
    batting_avg = models.FloatField(default=0)
    batting_best = models.BigIntegerField(default=0)
    strike_rate = models.FloatField(default=0)
    hundreds = models.BigIntegerField(default=0)
    fifties = models.BigIntegerField(default=0)
    sixes = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    bowling_runs = models.BigIntegerField(default=0)
    bowling_innings = models.BigIntegerField(default=0)
    wickets = models.BigIntegerField(default=0)
    bowling_avg = models.FloatField(default=0)
    bowling_best = models.FloatField(default=0)
    economy = models.FloatField(default=0)

    def __str__(self):
        return self.player.get_full_name()


class PerformanceMatchWise(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    match = models.ForeignKey('tournament.Match', on_delete=models.CASCADE, null=True)
    tournament = models.ForeignKey('tournament.Tournament', on_delete=models.CASCADE, null=True)
    team = models.ForeignKey('tournament.Team', on_delete=models.CASCADE, null=True)
    batting_runs = models.BigIntegerField(default=0)
    strike_rate = models.FloatField(default=0)
    sixes = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    bowling_runs = models.BigIntegerField(default=0)
    batting_balls = models.BigIntegerField(default=0)
    bowling_overs = models.BigIntegerField(default=0)
    wickets = models.BigIntegerField(default=0)
    bowling_avg = models.FloatField(default=0)
    economy = models.FloatField(default=0)
    status = models.CharField(max_length=20)

