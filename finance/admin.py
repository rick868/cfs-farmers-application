from django.contrib import admin

from .models import InsurancePolicy, LoanRequest


@admin.register(LoanRequest)
class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "farmer", "amount", "purpose", "status", "created_at")
    list_filter = ("status", "purpose", "created_at")
    search_fields = ("farmer__username", "farmer__email", "purpose")
    ordering = ("-created_at",)


@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ("id", "farmer", "crop_type", "coverage_amount", "premium_paid", "status", "start_date")
    list_filter = ("status", "crop_type", "start_date")
    search_fields = ("farmer__username", "farmer__email", "crop_type")
    ordering = ("-start_date",)
