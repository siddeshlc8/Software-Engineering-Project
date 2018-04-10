from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [

    path('', views.search, name='search'),
    path('<int:id>/', views.player, name='player'),
    path('nav-search-players/', views.nav_search_players, name='nav_search_players'),
    path('nav-search-matches/', views.nav_search_matches, name='nav_search_matches'),
    path('nav-search-organizers/', views.nav_search_organizers, name='nav_search_organizers'),
    path('nav-search-teams/', views.nav_search_teams, name='nav_search_teams'),
    path('nav-search-tournaments/', views.nav_search_tournaments, name='nav_search_tournaments'),
    path('tournaments/', views.search_tournaments, name='search_tournaments'),
    path('tournaments/details/<int:tournament_id>/', views.tournaments_details, name='tournaments_details'),
    path('tournaments/details/<int:tournament_id>/matches', views.tournaments_matches, name='tournaments_matches'),
    path('teams/', views.search_teams, name='search_teams'),
    path('teams/details/<int:team_id>/', views.teams_details, name='teams_details'),
    path('match/details/<int:match_id>/',views.match_details,name='match_details'),
    path('players/', views.search_players, name='search_players'),
    path('players/details/<int:player_id>/', views.player_details, name='player_details'),
    path('organizers/', views.search_organizers, name='search_organizers'),

]