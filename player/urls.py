from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='player_signup'),
]