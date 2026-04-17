from django.db import models
from users.models import Player
from uuid import uuid4

class Uniform(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, editable=False, max_length=50)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    number = models.CharField(max_length=2)
    size = models.CharField(max_length=10)