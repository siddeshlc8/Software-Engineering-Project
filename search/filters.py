from player.models import Player
from organizer.models import Organizer
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


class OrganizerFilter(django_filters.FilterSet):

    class Meta:
        model = Organizer
        fields = {
            'first_name': ['icontains']}