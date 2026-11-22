from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rent_price")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)