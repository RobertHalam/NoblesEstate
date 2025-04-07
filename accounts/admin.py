#admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NormalUser, RealtorUser

class NormalUserAdmin(UserAdmin):
    model = NormalUser
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff','is_email_verified')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name' ,'avatar')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )


class RealtorUserAdmin(UserAdmin):
    model = RealtorUser
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff','is_email_verified')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

# Register the custom admin classes
admin.site.register(NormalUser, NormalUserAdmin)
admin.site.register(RealtorUser, RealtorUserAdmin)
