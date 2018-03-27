from django.urls import path
from . import views

app_name = 'player'
urlpatterns = [

    path('home/', views.player_home, name='player_home'),
    path('view-profile/', views.player_view_profile, name='player_view_profile'),
    path('edit-profile/', views.player_edit_profile, name='player_edit_profile'),
    path('view-performance/',views.player_performance, name='player_view_performance'),
    path('password-change/', views.player_change_password, name='player_change_password'),
    path('password-change-done/', views.player_change_password_done, name='player_change_password_done'),
    path('my-tournaments/', views.my_tournaments, name='my_tournaments'),
    path('my-matches/', views.my_matches, name='my_matches'),

]

