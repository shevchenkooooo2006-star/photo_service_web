from django.contrib import admin
from .models import Photographer


@admin.register(Photographer)
class PhotographerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rating", "hourly_rate", "min_hours")
    list_display_links = ("id", "name")
    list_editable = ("rating", "hourly_rate")
    search_fields = ("name",)
    list_filter = ("min_hours",)
    ordering = ("-rating",)