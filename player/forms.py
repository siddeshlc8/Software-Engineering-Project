from django import forms
from .models import Player
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _


class PlayerSignUpForm(UserCreationForm):

    class Meta:
        model = Player
        fields = [
            'first_name',
            'last_name',
            'dob',
            'phone_no',
            'nationality',
            'state',
            'district',
            'player_type',
            'username',
            'password1',
            'password2',
            'email'
        ]

        labels = {
            'dob': _('Date of Birth'),
        }


class PlayerProfileForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = [
            'first_name',
            'last_name',
            'phone_no',
            'email',
            'nationality',
            'state',
            'district'
        ]

