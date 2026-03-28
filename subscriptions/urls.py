from django.urls import path
from .views import *

urlpatterns = [
    path('', new_subscription, name='add-subscription'),
    path('subscriptions-list', list_subscriptions, name='subscriptions-list'),
    path('ajax/get-subscriptions', get_subscriptions, name='get-subscriptions'),
    path('ajax/get-players', get_players, name='get-players')
]