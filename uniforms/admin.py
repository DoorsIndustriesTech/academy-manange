from django.contrib import admin
from .models import *

class PaymentInline(admin.TabularInline):
    model = UniformPayment
    extra = 1

class UniformAdmin(admin.ModelAdmin):
    inlines = [PaymentInline]

admin.site.register(Uniform,UniformAdmin)
