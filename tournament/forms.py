from django import forms
from .models import Team, Tournament, Match, Score


class TeamCreationForm(forms.ModelForm):
    logo = forms.ImageField(required=False)

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


class MatchCreationForm(forms.ModelForm):

    def __init__(self, tournament, *args, **kwargs):
        super(MatchCreationForm, self).__init__(*args, **kwargs)
        self.fields['team_1'] = forms.ModelChoiceField(
            queryset=Team.objects.filter(tournament=tournament)
        )
        self.fields['team_2'] = forms.ModelChoiceField(
            queryset=Team.objects.filter(tournament=tournament)
        )

    class Meta:
        model = Match
        fields = [
            'team_1',
            'team_2',
            'overs'
        ]


class ScoreForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = [

            'innings',
            'batting_team',
            'bowling_team' ,
            'ball_number' ,
            'over_number',
            'run',
            'extra_type',
            'extra_run',
            'is_wicket',
            'wicket_type'
        ]
