from django.urls import path
from . import views


app_name = 'recruit'

urlpatterns = [
    path('players', views.player_list, name='player_list'),
    path('coaches', views.coach_list, name='coach_list'),
    path('', views.home, name='home'),
    path('register', views.registration_view, name='register'),
    path('playerdetail/<int:pk>', views.PlayerDetail.as_view(), name="playerdetail"),
    path('coach/<int:id>', views.CoachDetail, name="coachdetail"),
    path('playerdetail/<int:id>/print', views.PlayerPrint, name='playerprint'),
]
