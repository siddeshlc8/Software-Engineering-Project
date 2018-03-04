from django.urls import path, include
from search import views as search_views
from organizer import views

app_name = 'organizer'
urlpatterns=[
    path('home/',views.home,name='home'),
    path('view_profile/',views.view_profile,name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('organizer_change_password/',views.organizer_change_password,name='change_password'),
]