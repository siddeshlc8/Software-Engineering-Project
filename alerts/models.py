from django.db import models

# Create your models here.

from tournament.models import  Tournament

class TournamentAlerts(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    title=models.CharField(max_length=20)
    body=models.CharField(max_length=100)
    posted_at=models.DateTimeField(auto_now_add=True)
