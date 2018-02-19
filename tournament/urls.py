from django.urls import path
from . import views

app_name = 'tournament'
urlpatterns = [
    path('', views.team, name='team'),
    path('team/<int:team_id>/', views.team_players, name='team_players'),
    path('team/<int:team_id>/<int:player_id>/', views.team_players_add, name='team_players_add'),

]