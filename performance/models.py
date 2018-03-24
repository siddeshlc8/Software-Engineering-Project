from django.db import models
from player.models import Player


class PerformanceTotal(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
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


class BattingInnings(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    match = models.ForeignKey('tournament.Match', on_delete=models.CASCADE, null=True, blank=True)
    tournament = models.ForeignKey('tournament.Tournament', on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey('tournament.Team', on_delete=models.CASCADE, null=True, blank=True)
    batting_runs = models.BigIntegerField(default=0)
    strike_rate = models.FloatField(default=0)
    sixes = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    batting_balls = models.BigIntegerField(default=0)
    status = models.CharField(max_length=20)
    out = models.BooleanField(default=False)
    out_type = models.CharField(max_length=20)
    played = models.BooleanField(default=False)
    started_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.player.get_full_name() + ' - ' + self.match.name


class BowlingInnings(models.Model):
    player = models.ForeignKey(Player, related_name='player', on_delete=models.CASCADE, null=True,
                               blank=True)
    match = models.ForeignKey('tournament.Match', on_delete=models.CASCADE, null=True, blank=True)
    tournament = models.ForeignKey('tournament.Tournament', on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey('tournament.Team', on_delete=models.CASCADE, null=True, blank=True)
    bowling_runs = models.BigIntegerField(default=0)
    batting_balls = models.BigIntegerField(default=0)
    bowling_overs = models.BigIntegerField(default=0)
    wickets = models.BigIntegerField(default=0)
    wickets_players = models.ManyToManyField(Player, related_name='wicket_players')
    bowling_avg = models.FloatField(default=0)
    economy = models.FloatField(default=0)
    played = models.BooleanField(default=False)
    started_time = models.DateTimeField(blank=True, null=True)






