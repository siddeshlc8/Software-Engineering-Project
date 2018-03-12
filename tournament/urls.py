from django.urls import path
from . import views

app_name = 'tournament'
urlpatterns = [
    path('create-tournament/', views.create_tournament, name='create_tournament'),
    path('create-team/<int:tournament_id>/', views.create_team, name='create_team'),
    path('', views.tournament, name='tournament'),
    path('<int:tournament_id>/', views.current_tournament, name='current_tournament'),
    path('<int:tournament_id>/edit', views.tournament_info_edit, name='tournament_info_edit'),
    path('team/<int:team_id>/', views.team_players, name='team_players'),
    path('team/<int:team_id>/<int:player_id>/', views.team_players_add, name='team_players_add'),
    path('<int:tournament_id>/create_match',views.create_match,name='create_match'),
    path('<int:tournament_id>/matches', views.all_matches, name='all_matches'),
    path('<int:tournament_id>/<int:match_id>/match', views.match, name='match'),
    path('<int:tournament_id>/<int:match_id>/<int:batting_team_id>/<int:bowling_team_id>/<int:innings>/enter_score',
         views.enter_score, name='enter_score'),
    path('<int:tournament_id>/<int:match_id>/submit_match', views.submit_match, name='submit_match'),
    path('<int:tournament_id>/submit_tournament', views.submit_tournament, name='submit_tournament'),
    path('<int:tournament_id>/create_schedule/', views.create_schedule, name='create_schedule')
]