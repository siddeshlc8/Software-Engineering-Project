from django.contrib import messages
from django.shortcuts import render, redirect
from organizer.models import Organizer
from tournament.models import Tournament
from alerts.models import TournamentAlerts
from .forms import TournamentAlertForm
# Create your views here.

def tournament_alerts(request, tournament_id):
    try:
        o = Organizer.objects.get(pk=request.user.id)
        current_tournament = Tournament.objects.get(pk=tournament_id)
        all_alerts=current_tournament.tournamentalerts_set.all()
        context = {'all_alerts':all_alerts, 'O': o,'current__tournament':current_tournament}
        return render(request, 'all_alerts.html', context)
    except Exception:
        return redirect('login')


def create_tournament_alert(request,tournament_id):
   try:
        organizer = Organizer.objects.get(pk=request.user.id)
        tournament=Tournament.objects.get(pk=tournament_id)
        if request.method == 'POST':
            form = TournamentAlertForm(request.POST)
            if form.is_valid():
                new_alert = form.save(commit=False)
                new_alert.tournament =tournament
                new_alert.save()
                messages.success(request,'alert sucessfully posted')
                return redirect('tournament:alerts:tournament_alerts',tournament_id)
            else:
                messages.warning(request,'give proper information')
                return render(request, 'all_alerts.html', {'form':form})
        else:
            form = TournamentAlertForm()
            context = {'form': form}
            return render(request, 'create_alert.html', context)
   except Exception:
         return redirect('login')
