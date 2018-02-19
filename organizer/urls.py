from django.urls import path

from organizer import views

app_name = 'organizer'
urlpatterns=[

    path('',views.organizers_page,name='orgainzers_page'),
    path('signup/',views.signup,name='signup'),
    path('<int:organizer_id>/home/',views.home,name='home'),
    path('<int:organizer_id>/view_profile',views.view_profile,name='view_profile'),
    path('<int:organizer_id>/edit_profile', views.edit_profile, name='edit_profile'),
    path('login/',views.login,name='login'),
    path('logout/',views.login,name='logout')

]