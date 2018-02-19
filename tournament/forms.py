from django import forms
from .models import Team, Tournament


class TeamCreationForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = [
            'name',
            'owner',
            'logo'
        ]
        labels = {
            'name': 'Team Name',
            'owner': 'Team Owner',
            'logo': 'Team Logo'
        }


class TournamentCreationForm(forms.ModelForm):
    place = forms.CharField(widget=forms.Textarea, max_length=100)

    class Meta:
        model = Tournament
        fields = [
            'name',
            'place',
            'start_date',
            'end_date'
        ]
        labels = {
            'name': 'Tournament Name',
            'start_date': 'Tournament Starting Date',
            'end_date': 'Tournament Ending Date'
        }