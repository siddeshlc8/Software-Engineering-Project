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

    def profile(self):
        value = {
            'First Name': getattr(self, 'first_name'),
            'Last Name': getattr(self, 'last_name'),
            'Phone Number': getattr(self, 'phone_no'),
            'Email Address': getattr(self, 'email'),
            'Nationality': getattr(self, 'nationality'),
            'State': getattr(self, 'state'),
            'District': getattr(self, 'district')}
        return value

    def details(self):
        value = {
            'First Name': getattr(self, 'first_name'),
            'Last Name': getattr(self, 'last_name'),
            'Player Type': getattr(self, 'player_type')}
        return value







