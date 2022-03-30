from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


@admin.register(Account)
class AccountAdmin(UserAdmin):
    ordering = ['-date_join']
    list_display = ['email', 'first_name', 'last_name', 'username', 'last_login', 'is_active', 'date_join']
    filter_horizontal = []
    list_filter = ['email', 'first_name', 'last_name', 'username', 'last_login', 'is_active', 'date_join']
    search_fields = ['email', 'first_name', 'last_name', 'username', 'last_login', 'is_active', 'date_join']
    fieldsets = []
    list_display_links = ['email', 'first_name', 'last_name']
    readonly_fields = ['last_login', 'date_join']
    list_per_page = 10


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'state', 'country', 'img']
    search_fields = ['user', 'address_line1', 'city', 'state', 'country']
    readonly_fields = ['img', ]
    list_per_page = 10
