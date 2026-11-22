from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id", "client", "photographer", "location",
        "shoot_date", "hours", "is_cancelled",
    )
    list_display_links = ("id",)
    list_filter = ("is_cancelled", "shoot_date", "need_makeup")
    search_fields = ("client__name", "photographer__name", "location__name")
    autocomplete_fields = ("client", "photographer", "location")
    date_hierarchy = "shoot_date"
    ordering = ("-shoot_date",)