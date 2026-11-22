from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Client


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "email", "role", "is_staff")
    list_filter = ("role", "is_staff")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Роль", {"fields": ("role",)}),
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "user")
    list_display_links = ("id", "name")
    search_fields = ("name", "email")
    autocomplete_fields = ("user",)