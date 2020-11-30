from django.urls import path
from . import views


app_name = 'recruit'

urlpatterns = [
    # path('players', views.player_list, name='player_list'),
    # path('coaches', views.coach_list, name='coach_list'),
    path('', views.home, name='home'),
    path('register', views.RegistrationFrom, name='register'),
    # path('player/<int:pk>', views.PlayerDetail.as_view(), name="detail"),
    # path('coach/<int:id>', views.CoachDetail, name="coachdetail"),
    # path('player/<int:id>/print', views.PlayerPrint, name='playerprint'),
]
