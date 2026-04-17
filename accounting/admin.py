from django.contrib import admin
from .models import Outcoming, Subscription, UniformPayment

admin.site.register(Outcoming)

admin.site.register(Subscription)

admin.site.register(UniformPayment)