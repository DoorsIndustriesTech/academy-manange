from django.contrib import admin
from .models import *
from accounting.models import Subscription
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 1
    # readonly_fields = ['expiration_date']
    can_delete = True

class PlayerResource(resources.ModelResource):
    class Meta:
        model = Player
        fields = ('id', 'primary_name', 'secondary_name', 'first_last_name', 'second_last_name', 'dob', 'gender', 'phone')

@admin.register(Player)
class PlayerAdmin(ImportExportModelAdmin):
    resource_class = PlayerResource
    inlines = [SubscriptionInline]
    readonly_fields = ('created_date',)
    list_display = ('primary_name', 'first_last_name','dob','phone')

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('primary_name', 'first_last_name','phone')

@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    list_display = ('first_name','last_name','username','email', 'phone')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone','job_position','gender','photo','school')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','username','email', 'password1', 'password2')}
        ),
    )

@admin.register(School)
class School(admin.ModelAdmin):
    pass
