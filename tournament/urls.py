from django.urls import path
from . import views

app_name = 'tournament'
urlpatterns = [
    path('create-tournament/<int:organizer_id>/', views.create_tournament, name='create_tournament'),
    path('create-team/<int:organizer_id>/<int:tournament_id>/', views.create_team, name='create_team'),
    path('<int:organizer_id>/', views.tournament, name='tournament'),
    path('<int:organizer_id>/<int:tournament_id>/', views.tournament_teams, name='tournament_teams'),
    path('team/<int:team_id>/', views.team_players, name='team_players'),
    path('team/<int:team_id>/<int:player_id>/', views.team_players_add, name='team_players_add'),
    path('<int:tournament_id>/create_match',views.create_match,name='create_match'),
    path('<int:tournament_id>/matches', views.all_matches, name='all_matches'),
    path('<int:tournament_id>/<int:match_id>/match', views.match, name='match'),
    path('<int:tournament_id>/<int:match_id>/enter_score', views.enter_score, name='enter_score'),
    path('<int:tournament_id>/<int:match_id>/score', views.scores, name='scores'),
]