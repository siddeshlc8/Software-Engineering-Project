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

    def __init__(self, tournament, match, batting, bowling,*args, **kwargs):
        super(ScoreForm, self).__init__(*args, **kwargs)
        self.fields['batting_team'] = forms.ChoiceField(
            choices=[(match.team_1.id, str(match.team_1)), (match.team_2.id, str(match.team_2))]
        )
        self.fields['bowling_team'] = forms.ChoiceField(
            choices=[(match.team_2.id, str(match.team_2)), (match.team_1.id, str(match.team_1))]
        )
        self.fields['bowler'] = forms.ChoiceField(
            choices=[(player.id, str(player)) for player in Team.objects.get(id=bowling.id).players.all()]
        )
        self.fields['batsman'] = forms.ChoiceField(
            choices=[(player.id, str(player)) for player in Team.objects.get(id=batting.id).players.all()]
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


class ScoreUpdateForm(forms.Form):
    def __init__(self, batting, bowling, *args, **kwargs):
        super(ScoreUpdateForm, self).__init__(*args, **kwargs)
        self.fields['bowler'] = forms.ChoiceField(
            choices=[(player.id, str(player)) for player in Team.objects.get(id=bowling.id).players.all()]
        )
        self.fields['batsman'] = forms.ChoiceField(
            choices=[(player.id, str(player)) for player in Team.objects.get(id=batting.id).players.all()]
        )
        self.fields['extra_type'] = forms.ChoiceField(
            choices=[
                ('Wide', 'Wide'),
                ('NoBall', 'NoBall'),
                ('DeadBall', 'DeadBall')
            ]
        )
        self.fields['wicket_type'] = forms.ChoiceField(
            choices=[
                ('RunOut', 'RunOut'),
                ('Catch', 'Catch'),
                ('Bowled', 'Bowled'),
                ('Lbw', 'Lbw'),
                ('Stumps', 'Stumps'),
                ('HitWicket', 'HitWicket')
            ]
        )

    ball_number = forms.IntegerField()
    over_number = forms.IntegerField()
    bowler = forms.CharField(max_length=11)
    batsman = forms.CharField(max_length=11)
    run = forms.IntegerField(required=False)
    extra_type = forms.CharField(max_length=11, required=False,)
    extra_run = forms.IntegerField(required=False)
    is_wicket = forms.BooleanField(required=False)
    wicket_type = forms.CharField(max_length=11, required=False)



