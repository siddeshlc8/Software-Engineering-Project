from django.urls import path, include

from . import views


app_name = 'tournament'
urlpatterns = [
    path('create-tournament/', views.create_tournament, name='create_tournament'),
    path('create-team/<int:tournament_id>/', views.create_team, name='create_team'),
    path('', views.tournament, name='tournament'),
    path('<int:tournament_id>/', views.current_tournament, name='current_tournament'),
    path('<int:tournament_id>/edit', views.tournament_info_edit, name='tournament_info_edit'),
    path('team/<int:team_id>/', views.team_players, name='team_players'),
    path('team/<int:team_id>/add_players', views.add_players, name='add_players'),
    path('team/<int:team_id>/<int:player_id>/', views.team_players_add, name='team_players_add'),
    path('<int:tournament_id>/create_match',views.create_match,name='create_match'),
    path('<int:tournament_id>/matches', views.all_matches, name='all_matches'),

    path('<int:match_id>/match', views.match, name='match'),
    path('<int:match_id>/match/overs/', views.match_overs, name='match_overs'),
    path('<int:match_id>/match/toss/', views.match_toss, name='match_toss'),
    path('<int:match_id>/match/select-openers/', views.match_openers,
         name='match_openers'),

    path('<int:match_id>/enter_score', views.enter_score, name='enter_score'),
    path('<int:match_id>/live-score', views.live_scores, name='live_scores'),
    path('<int:match_id>/select-new-batsman', views.select_new_batsman, name='select_new_batsman'),
    path('<int:match_id>/select-new-bowler', views.select_new_bowler, name='select_new_bowler'),

    path('<int:match_id>/submit_match', views.submit_match, name='submit_match'),
    path('<int:match_id>/submit-innings/', views.submit_innings, name='submit_innings'),
    path('<int:tournament_id>/submit_tournament', views.submit_tournament, name='submit_tournament'),
    path('<int:tournament_id>/create_schedule/', views.create_schedule, name='create_schedule'),
    path('<int:match_id>/start_match/', views.start_match, name='start_match'),
    path('<int:tournament_id>/start_tournament/', views.start_tournament, name='start_tournament'),
    path('<int:tournament_id>/alerts',include('alerts.urls'), name='tournament_alerts'),



]