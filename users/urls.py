from django.urls import path
from .views import *

urlpatterns = [
    path('register/', adminRegistration, name='register'),
    path('get-players-list/', get_players_list, name="get_players_list"),
    path('register-player/', register_player, name="register_player"),
    path('players-list/', players_list, name='players_list'),
    path('player/<id>/detail/', player_detail, name='player_detail'),
    path('edit-player/<id>/', edit_player, name='edit_player'),
    path('get-uniforms-list/', get_uniform_list, name="get_uniforms_list"),
    path('uniforms-list/', uniforms_list, name='uniforms_list'),
    path('ajax/get-orders-list/', get_orders_list, name='get_orders_list'),
]