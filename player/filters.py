from .models import Player
from tournament.models import Tournament, Team
import django_filters


class PlayerFilter(django_filters.FilterSet):

    class Meta:
        model = Player
        fields = {
            'first_name': ['icontains'],
            'player_type': ['exact']}


class TournamentFilter(django_filters.FilterSet):

    class Meta:
        model = Tournament
        fields = {
            'name': ['icontains'],
            'place': ['icontains']}


class TeamFilter(django_filters.FilterSet):

    class Meta:
        model = Team
        fields = {
            'name': ['icontains']}