from django.shortcuts import render
from .forms import PlayerSignUpForm
from .models import Player


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = PlayerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'player/registration/signup.html')
    else:
        form = PlayerSignUpForm()
    return render(request, 'player/registration/signup.html', {'form': form})

