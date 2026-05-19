from django.urls import path
from .views import adminRegistration, loginUser, get_players_list, register_player, players_list, player_detail, edit_player

urlpatterns = [
    path('', loginUser, name='login'),
    path('register', adminRegistration, name='registration'),
    path('get-players-list', get_players_list, name="get_players_list"),
    path('register-player', register_player, name="register_player"),
    path('players-list', players_list, name='players_list'),
    path('player/<id>/detail', player_detail, name='player_detail'),
    path('edit-player/<id>/', edit_player, name='edit_player')
]