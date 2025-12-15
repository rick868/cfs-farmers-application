from django.contrib import admin

from .models import (
    FarmerGroup,
    FarmerInquiry,
    FollowUpFlag,
    GroupMembership,
    SoilTest,
    TraceabilityRecord,
    YieldLog,
)


@admin.register(FarmerInquiry)
class FarmerInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "crop",
        "preferred_contact",
        "contact_value",
        "status",
        "created_at",
    )
    list_filter = ("status", "preferred_contact", "created_at")
    search_fields = ("name", "location", "crop", "question", "contact_value")
    ordering = ("-created_at",)


@admin.register(FollowUpFlag)
class FollowUpFlagAdmin(admin.ModelAdmin):
    list_display = ("farmer", "topic", "priority", "status", "due_date", "updated_at")
    list_filter = ("priority", "status", "due_date")
    search_fields = ("farmer__username", "farmer__email", "topic", "note")
    ordering = ("-updated_at",)


@admin.register(SoilTest)
class SoilTestAdmin(admin.ModelAdmin):
    list_display = ("sample_label", "farmer", "crop", "ph", "created_at")
    list_filter = ("crop", "created_at")
    search_fields = ("sample_label", "farmer__username", "farmer__email", "location", "crop", "notes")
    ordering = ("-created_at",)


@admin.register(YieldLog)
class YieldLogAdmin(admin.ModelAdmin):
    list_display = ("crop", "season", "area_acres", "yield_qty", "region", "created_at")
    list_filter = ("crop", "region", "season")
    search_fields = ("crop", "region", "season", "farmer__username", "farmer__email")
    ordering = ("-created_at",)


@admin.register(FarmerGroup)
class FarmerGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "purpose", "contact_phone", "created_at")
    search_fields = ("name", "region", "purpose", "contact_phone")
    ordering = ("-created_at",)


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ("group", "user", "role", "joined_at")
    list_filter = ("role",)
    search_fields = ("group__name", "user__username", "user__email")
    ordering = ("-joined_at",)


@admin.register(TraceabilityRecord)
class TraceabilityRecordAdmin(admin.ModelAdmin):
    list_display = ("batch_code", "crop", "farmer", "harvest_date", "created_at")
    list_filter = ("crop", "harvest_date", "created_at")
    search_fields = ("batch_code", "crop", "farmer__username", "farmer__email", "location", "description")
    ordering = ("-created_at",)
