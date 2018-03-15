"""cricket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'cricket'
urlpatterns = [
    path('player_page/', views.players_page, name='players_page'),
    path('player_signup/', views.player_signup, name='player_signup'),
    path('organizer_signup/', views.organizer_signup, name='organizer_signup'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('organizer_page/', views.organizers_page, name='organizers_page'),
    path('search/', include('search.urls'), name='search'),
    path('admin/', admin.site.urls),
    path('player/', include('player.urls'), name='player'),
    path('organizer/',include('organizer.urls'),name='organizer'),
    path('', views.home_page, name='home_page'),
    path('live/', views.live ,name='live'),
    path('tournament/', include('tournament.urls'), name='tournament'),
    path('home/',views.home,name='home')
]
