from django.db import models
from django.contrib.auth.models import User


class Player(User):

    PLAYER_TYPE_CHOICES = [
        ('Batsman', 'Batsman'),
        ('Bowler', 'Bowler'),
        ('All_Rounder', 'All_Rounder')
    ]
    player_type = models.CharField(max_length=11, choices=PLAYER_TYPE_CHOICES)
    phone_no = models.CharField(max_length=10)
    nationality = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    dob = models.DateField()





