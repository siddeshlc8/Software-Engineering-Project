from django import forms
from .models import Team, Tournament, Match, Score
from player.models import Player
from performance.models import BattingInnings, BowlingInnings



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
    #place = forms.CharField(widget=forms.Textarea, max_length=100)

    class Meta:
        model = Tournament
        fields = [
            'name',
            'place',
            'start_date',
            'end_date',
            'image',
        ]
        labels = {
            'name': 'Tournament Name',
            'start_date': 'Tournament Starting Date',
            'end_date': 'Tournament Ending Date',
            'image' : 'Select an Image',
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


class ScoreUpdateForm(forms.Form):
    def __init__(self, player1, player2, *args, **kwargs):
        super(ScoreUpdateForm, self).__init__(*args, **kwargs)
        if player1 is not None and player2 is not None:
            self.fields['batsman'] = forms.ChoiceField(
                choices=[(player1.player.id, str(player1.player)), (player2.player.id, str(player2.player))]
            )
            self.fields['out_batsman'] = forms.ChoiceField(
                choices=[(player1.player.id, str(player1.player)), (player2.player.id, str(player2.player))]
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
    over_number = forms.IntegerField(initial='class')
    batsman = forms.CharField(max_length=11)
    run = forms.IntegerField(required=False)
    extra_type = forms.CharField(max_length=11, required=False,)
    extra_run = forms.IntegerField(required=False)
    is_wicket = forms.BooleanField(required=False)
    wicket_type = forms.CharField(max_length=11, required=False)
    six = forms.BooleanField(required=False)
    four = forms.BooleanField(required=False)
    out_batsman = forms.CharField(max_length=11)
    commentary = forms.CharField(widget=forms.Textarea(attrs={'cols': '70', 'rows': '3'}))
    is_extra = forms.BooleanField(required=False)


class SelectBatsmanForm(forms.Form):
    def __init__(self, players, *args, **kwargs):
        super(SelectBatsmanForm, self).__init__(*args, **kwargs)
        if players is not None:
            self.fields['player'] = forms.ChoiceField(
                choices=[(player.player.id, str(player.player)) for player in players]
            )

    player = forms.CharField(max_length=12)


class SelectBowlerForm(forms.Form):
    def __init__(self, players, *args, **kwargs):
        super(SelectBowlerForm, self).__init__(*args, **kwargs)
        if players is not None:
            self.fields['player'] = forms.ChoiceField(
                choices=[(player.player.id, str(player.player)) for player in players]
            )

    player = forms.CharField(max_length=12)


class TossForm(forms.Form):
    def __init__(self, match, *args, **kwargs):
        super(TossForm, self).__init__(*args, **kwargs)
        self.fields['toss_winner'] = forms.ChoiceField(
            choices=[ (match.team_1.id, str(match.team_1)), (match.team_2.id, str(match.team_2))]
        )
        self.fields['toss_winner_choice'] = forms.ChoiceField(
            choices=[('Batting', 'Batting'),
                     ('Bowling', 'Bowling')]
        )

    toss_winner = forms.CharField(max_length=11)
    toss_winner_choice = forms.CharField(max_length=10)


class OverForm(forms.Form):
    overs = forms.IntegerField()


class OpenerForm(forms.Form):
    def __init__(self, team, *args, **kwargs):
        super(OpenerForm, self).__init__(*args, **kwargs)
        self.fields['striker'] = forms.ChoiceField(
            choices=[(player.id, str(player)) for player in team.players.all()]
        )
        self.fields['non_striker'] = forms.ChoiceField(
            choices=[(player.id, str(player)) for player in team.players.all()]
        )

    striker = forms.CharField(required=False)
    non_striker = forms.CharField(required=False)


class WinnerForm(forms.Form):
    def __init__(self, team1, team2, *args, **kwargs):
        super(WinnerForm, self).__init__(*args, **kwargs)
        self.fields['winner'] = forms.ChoiceField(
            choices=[(team1.id, str(team1)), (team2.id, str(team2))]
        )

    winner = forms.CharField(required=False)


