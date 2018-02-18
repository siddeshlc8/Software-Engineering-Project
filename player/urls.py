from django.urls import path
from . import views

app_name = 'player'
urlpatterns = [
    path('', views.players_page, name='players_page'),
    path('home/', views.player_home, name='player_home'),
    path('signup/', views.player_signup, name='player_signup'),
    path('login/', views.player_login, name='player_login'),
    path('logout/', views.player_logout, name='player_logout'),
    path('view-profile/', views.player_view_profile, name='player_view_profile'),
    path('edit-profile/', views.player_edit_profile, name='player_edit_profile'),
    path('password-change/', views.player_change_password, name='player_change_password'),
    path('password-change-done/', views.player_change_password_done, name='player_change_password_done'),
]