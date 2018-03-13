from django.urls import path, include


from alerts import views

app_name = 'alerts'
urlpatterns=[




    path('',views.tournament_alerts,name='tournament_alerts'),
    path('create_alert/',views.create_tournament_alert,name='create_tournament_alert'),

]