from .models import Organizer
import django_filters


class OrganizerFilter(django_filters.FilterSet):

    class Meta:
        model = Organizer
        fields = {
            'first_name': ['icontains']}
