from django.urls import path

from organizer import views

app_name = 'organizer'
urlpatterns=[

    path('',views.organizers_page,name='orgainzers_page'),
    path('signup/',views.signup,name='signup'),
    path('<int:organizer_id>/home/',views.home,name='home')

]