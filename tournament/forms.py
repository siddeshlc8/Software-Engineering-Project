from django import forms
from .models import Team, Tournament, Match, Score
from player.models import Player



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

    def __init__(self, tournament, match, batting,bowling,*args, **kwargs):
        super(ScoreForm, self).__init__(*args, **kwargs)
        self.fields['batting_team'] = forms.ChoiceField(
            choices=[(match.team_1.id, str(match.team_1)), (match.team_2.id, str(match.team_2))]
        )
        self.fields['bowling_team'] = forms.ChoiceField(
            choices=[(match.team_2.id, str(match.team_2)), (match.team_1.id, str(match.team_1))]
        )
        self.fields['batsman'] = forms.ModelChoiceField(
            queryset=Player.objects.filter(team=batting)
        )
        self.fields['bowler'] = forms.ModelChoiceField(
            queryset=Player.objects.filter(team=bowling)
        )

    class Meta:
        model = Score
        fields = [

            'innings',
            'batting_team',
            'bowling_team' ,
            'ball_number' ,
            'over_number',
            'batsman',
            'bowler',
            'run',
            'extra_type',
            'extra_run',
            'is_wicket',
            'wicket_type'
        ]



class Submit_match_form(forms.Form):
     team1 = forms.CharField(label='team1 name', max_length=100)
     team2 = forms.CharField(label='team2 name', max_length=100)


class Submit_tournament_form(forms.Form):
    tournament_name = forms.CharField(label='tournament name', max_length=100)



