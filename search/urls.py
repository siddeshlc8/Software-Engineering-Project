from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [

    path('', views.search, name='search'),
    path('nav-search-players/', views.nav_search_players, name='nav_search_players'),
    path('nav-search-count/', views.nav_search_count, name='nav_search_count'),
    path('tournaments/', views.search_tournaments, name='search_tournaments'),
    path('tournaments/details/<int:tournament_id>/', views.tournaments_details, name='tournaments_details'),
    path('teams/', views.search_teams, name='search_teams'),
    path('teams/details/<int:team_id>/', views.teams_details, name='teams_details'),
    path('players/', views.search_players, name='search_players'),
    path('players/details/<int:player_id>/', views.player_details, name='player_details'),
    path('organizers/', views.search_organizers, name='search_organizers'),

]