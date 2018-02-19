from django.urls import path
from . import views

app_name = 'tournament'
urlpatterns = [
    path('create-tournament/', views.create_tournament, name='create_tournament'),
    path('', views.tournament, name='tournament'),
    path('<int:tournament_id>/', views.tournament_teams, name='tournament_teams'),
    path('team/<int:team_id>/', views.team_players, name='team_players'),
    path('team/<int:team_id>/<int:player_id>/', views.team_players_add, name='team_players_add'),

]