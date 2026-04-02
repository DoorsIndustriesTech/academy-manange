from django.shortcuts import render
from .models import Player
from .serializers import PlayerSerializer
from rest_framework import viewsets
from rest_framework_api_key.permissions import HasAPIKey

# def players_list(request, template = 'players/list.html')
class PlayerViewset(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer