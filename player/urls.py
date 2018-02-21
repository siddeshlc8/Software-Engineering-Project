from django.urls import path
from . import views

app_name = 'player'
urlpatterns = [
    path('', views.PlayerPageView.as_view(), name='players_page'),
    path('player-browse/', views.PlayerBrowseView.as_view(), name='player_browse'),
    path('home/', views.player_home, name='player_home'),
    path('signup/', views.player_signup, name='player_signup'),
    path('login/', views.player_login, name='player_login'),
    path('logout/', views.PlayerLogoutView.as_view(), name='player_logout'),
    path('search/', views.search, name='search'),
    path('search/tournaments/', views.search_tournaments, name='search_tournaments'),
    path('search/tournaments/details/<int:tournament_id>/', views.tournaments_details, name='tournaments_details'),
    path('search/teams/', views.search_teams, name='search_teams'),
    path('search/teams/details/<int:team_id>/', views.teams_details, name='teams_details'),
    path('search/players/', views.search_players, name='search_players'),
    path('search/players/details/<int:player_id>/', views.player_details, name='player_details'),
    path('view-profile/', views.player_view_profile, name='player_view_profile'),
    path('edit-profile/', views.player_edit_profile, name='player_edit_profile'),
    path('view-performance/',views.PlayerPerformanceView.as_view(), name='player_view_performance'),
    path('password-change/', views.player_change_password, name='player_change_password'),
    path('password-change-done/', views.player_change_password_done, name='player_change_password_done'),

]