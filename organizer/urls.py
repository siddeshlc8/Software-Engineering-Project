from django.urls import path

from organizer import views

app_name = 'organizer'
urlpatterns=[

    path('',views.organizers_page,name='organizers_page'),
    path('signup/',views.signup,name='signup'),
    path('home/',views.home,name='home'),
    path('view_profile/',views.view_profile,name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('login/',views.Org_login,name='login'),
    path('logout/',views.Org_logout,name='logout'),
    path('organizer_change_password/',views.organizer_change_password,name='change_password'),

]