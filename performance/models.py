from django.db import models
from player.models import Player


class PerformanceTotal(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournaments = models.BigIntegerField()
    matches = models.BigIntegerField()
    batting_innings = models.BigIntegerField()
    batting_runs = models.BigIntegerField()
    high_score = models.BigIntegerField()
    batting_avg = models.FloatField()
    batting_best = models.BigIntegerField()
    strike_rate = models.FloatField()
    hundreds = models.BigIntegerField()
    fifties = models.BigIntegerField()
    sixes = models.IntegerField()
    fours = models.IntegerField()
    bowling_runs = models.BigIntegerField()
    bowling_innings = models.BigIntegerField()
    wickets = models.BigIntegerField()
    bowling_avg = models.FloatField()
    bowling_best = models.FloatField()
    economy = models.FloatField()

    def __str__(self):
        return self.player.get_full_name()


class PerformanceMatchWise(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    batting_runs = models.BigIntegerField()
    strike_rate = models.FloatField(null=True)
    sixes = models.IntegerField(null=True)
    fours = models.IntegerField(null=True)
    bowling_runs = models.BigIntegerField(null=True)
    bowling_overs = models.BigIntegerField(null=True)
    wickets = models.BigIntegerField(null=True)
    bowling_avg = models.FloatField(null=True)
    economy = models.FloatField(null=True)

    def __str__(self):
        return self.name
