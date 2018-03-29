from django import forms
from .models import Organizer
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _


class OrganizerSignupForm(UserCreationForm):

    class Meta:
        model = Organizer
        fields = [
            'username',
            'password1',
            'password2',
            'email',
        ]


class OrganizerProfileForm(forms.ModelForm):

    class Meta:
        model = Organizer
        fields = [
            'username',
            'first_name',
            'last_name',
            'phone_no',
            'email',
            'nationality',
            'state',
            ]