from django.contrib import admin
from .models import *
from accounting.models import UniformPayment

class PaymentInline(admin.TabularInline):
    model = UniformPayment
    extra = 1

@admin.register(Uniform)
class UniformAdmin(admin.ModelAdmin):
    inlines = [PaymentInline]