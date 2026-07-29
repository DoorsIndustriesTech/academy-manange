from django.contrib import admin
from .models import Outcoming, Subscription, UniformPayment, Savings

admin.site.register(Outcoming)

admin.site.register(Subscription)

admin.site.register(UniformPayment)

admin.site.register(Savings)