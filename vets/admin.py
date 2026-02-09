from django.contrib import admin
from .models import Vet
from django.utils.html import format_html


@admin.register(Vet)
class VetAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "logo_preview",
        "postal_code",
    )
    
    # logo in form view
    readonly_fields = ("logo_preview",)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height: 100px; border-radius: 4px;" />',
                obj.logo.url
            )
        return "—"

    logo_preview.short_description = "Logo"
