from django.urls import path
from .views import *

urlpatterns = [
    path('', register_player, name="register_player")
]