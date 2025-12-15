from django.contrib import admin

from .models import PolicyDocument


@admin.register(PolicyDocument)
class PolicyDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "region", "category", "created_at")
    list_filter = ("region", "category", "created_at")
    search_fields = ("title", "region", "category")
    ordering = ("-created_at",)
