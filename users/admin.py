from django.contrib import admin
from .models import *
from subscriptions.models import Subscription

# Register your models here.
class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 1
    readonly_fields = ['expiration_date']
    can_delete = True

class PlayerAdmin(admin.ModelAdmin):
    inlines = [SubscriptionInline]
    readonly_fields = ('created_date',)
    list_display = ('primary_name', 'first_last_name','dob','phone')
admin.site.register(Player,PlayerAdmin)

class ParentAdmin(admin.ModelAdmin):
    list_display = ('primary_name', 'first_last_name','phone')
admin.site.register(Parent,ParentAdmin)