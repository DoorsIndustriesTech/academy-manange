from django.db import models
from uuid import uuid4
from uniforms.models import Uniform
from users.models import Player, School
from dateutil.relativedelta import relativedelta

class Outcoming(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, editable=False, max_length=50)
    school = models.ForeignKey(School,on_delete=models.PROTECT,null=True,blank=True)
    description = models.TextField(max_length=260,null=True,blank=True)
    amount = models.CharField(max_length=10,null=True,blank=True)
    date = models.DateField(null=True,blank=True)

PAYMENT_METHODS = ((0,'Digital'),(1,'Cash'))

class UniformPayment(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, editable=False, max_length=50)
    uniform = models.ForeignKey(Uniform, on_delete=models.CASCADE,null=True,blank=True)
    amount = models.CharField(max_length=7,null=True,blank=True)
    payment_method = models.IntegerField(choices=PAYMENT_METHODS,null=True,blank=True)
    pay_date = models.DateField(null=True,blank=True)

PHYSICAL_CONDITION_CHOICES = ((0, 'Good'), (1, 'Other'))

class Subscription(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, editable=False, max_length=50)
    player = models.ForeignKey(Player, on_delete=models.CASCADE,null=True,blank=True)
    physical_condition = models.IntegerField(choices=PHYSICAL_CONDITION_CHOICES,null=True,blank=True)
    condition = models.CharField(max_length=50, blank=True, null=True)
    single_class = models.BooleanField(default=False)
    ammount = models.CharField(max_length=10,null=True,blank=True)
    pay_date = models.DateField(null=True,blank=True)
    expiration_date = models.DateField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.pay_date and not self.single_class:
            self.expiration_date = self.pay_date + relativedelta(months=1)
        else:
            self.expiration_date = self.pay_date

        super().save(*args, **kwargs)
    
class Savings(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, editable=False, max_length=50)
    school = models.ForeignKey(School,on_delete=models.PROTECT,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    ammount = models.CharField(max_length=7, null=True, blank=True)