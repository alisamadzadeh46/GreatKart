from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


@admin.register(Account)
class AccountAdmin(UserAdmin):
    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name', 'username', 'last_login', 'is_active', 'date_join']
    filter_horizontal = []
    list_filter = ['email', 'first_name', 'last_name', 'username', 'last_login', 'is_active', 'date_join']
    search_fields = ['email', 'first_name', 'last_name', 'username', 'last_login', 'is_active', 'date_join']
    fieldsets = []
