from django import forms

from player.models import Player
from alerts.models import TournamentAlerts



class TournamentAlertForm(forms.ModelForm):


    class Meta:
        model = TournamentAlerts
        fields = [
            'title',
            'body',

        ]
        labels = {
            'title': 'Alert Title',
            'body': 'Alert Body',

        }