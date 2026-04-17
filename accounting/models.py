from django.db import models
from uuid import uuid4
from uniforms.models import Uniform
from users.models import Player
from dateutil.relativedelta import relativedelta

class Outcoming(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, editable=False, max_length=50)
    description = models.TextField(max_length=260)
    amount = models.CharField(max_length=10)
    date = models.DateField()

class UniformPayment(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, editable=False, max_length=50)
    uniform_id = models.ForeignKey(Uniform, on_delete=models.CASCADE)
    amount = models.CharField(max_length=7)
    pay_date = models.DateField()

PHYSICAL_CONDITION_CHOICES = (('GOOD', 'Good'), ('OTHER', 'Other'))

class Subscription(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, editable=False, max_length=50)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    physical_condition = models.CharField(max_length=6, choices=PHYSICAL_CONDITION_CHOICES)
    condition = models.CharField(max_length=50, blank=True, null=True)
    single_class = models.BooleanField(default=False)
    ammount = models.CharField(max_length=10)
    pay_date = models.DateField()
    expiration_date = models.DateField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.pay_date and str(self.single_class).upper() == 'NO':
            self.expiration_date = self.pay_date + relativedelta(months=1)
        else:
            self.expiration_date = self.pay_date

        super().save(*args, **kwargs)