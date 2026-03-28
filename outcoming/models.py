from django.db import models
from uuid import uuid4

class Outcoming(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, editable=False, max_length=50)
    description = models.TextField(max_length=260)
    amount = models.CharField(max_length=10)
    date = models.DateField()