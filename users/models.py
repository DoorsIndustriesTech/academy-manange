from django.db import models
from uuid import uuid4

class Player(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, editable=False, max_length=50)
    primary_name = models.CharField(max_length=50)
    secondary_name = models.CharField(max_length=50, blank=True, null=True)
    first_last_name = models.CharField(max_length=50)
    second_last_name = models.CharField(max_length=50, blank=True, null=True)
    dob = models.CharField(null=True, blank=True)
    phone = models.CharField(max_length=10)
    created_date = models.DateField(auto_now_add=True)
    def full_name(self):
        if self.secondary_name or self.second_last_name:
            return "%s %s %s %s" % (self.primary_name, self.secondary_name, self.first_last_name, self.second_last_name)
        else:
            return "%s %s" % (self.primary_name, self.first_last_name)
    
    def __str__(self):
        if self.secondary_name or self.second_last_name:
            return "%s %s %s %s" % (self.primary_name, self.secondary_name, self.first_last_name, self.second_last_name)
        else:
            return "%s %s" % (self.primary_name, self.first_last_name)
    
class Parent(models.Model):
    id = models.CharField(primary_key=True, max_length=50, default=uuid4, editable=False)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    primary_name = models.CharField(max_length=50)
    secondary_name = models.CharField(max_length=50, blank=True, null=True)
    first_last_name = models.CharField(max_length=50)
    second_last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=10)