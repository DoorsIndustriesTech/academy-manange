from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser 

GENDER_CHOICES = (('F', 'Femaie'), ('M', 'Male'))

JOB_CHOICES = (('Administrative', 'Administrative'), ('Coach', 'Coach'))

class School(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    photo = models.ImageField(upload_to='coaches', null=True, blank=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.PROTECT, null=True, blank=True)
    job_position = models.CharField(choices=JOB_CHOICES, null=True, blank=True)
    
    class Meta(object):
        unique_together = ('email',)

class Player(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, editable=False, max_length=50)
    coach = models.ForeignKey(User, on_delete=models.PROTECT,null=True, blank=True)
    primary_name = models.CharField(max_length=50)
    secondary_name = models.CharField(max_length=50, blank=True, null=True)
    first_last_name = models.CharField(max_length=50)
    second_last_name = models.CharField(max_length=50, blank=True, null=True)
    dob = models.CharField(null=True, blank=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, null=True, blank=True)
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