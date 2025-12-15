from django.contrib import admin

from .models import MarketListing


@admin.register(MarketListing)
class MarketListingAdmin(admin.ModelAdmin):
    list_display = ("crop_name", "seller", "quantity", "price_per_unit", "location", "created_at")
    list_filter = ("location", "created_at")
    search_fields = ("crop_name", "seller__username", "seller__email", "location")
    ordering = ("-created_at",)
