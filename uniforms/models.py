from django.db import models
from users.models import Player
from uuid import uuid4

class Uniform(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, editable=False, max_length=50)
    player = models.ForeignKey(Player, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=20,null=True,blank=True)
    number = models.IntegerField(null=True,blank=True)
    size = models.CharField(max_length=10,null=True,blank=True)