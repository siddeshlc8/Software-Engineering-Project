from django import forms
from .models import Player
from django.contrib.auth.forms import UserCreationForm


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
            'password1',
            'password2'
        ]