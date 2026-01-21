from django.contrib import admin
from .models import FosterHome

@admin.register(FosterHome)
class FosterHomeAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'city',
        'phone_number',
        'status',
        'has_other_cats',
        'has_dogs',
        'created_at',
    )

    # filter_horizontal = ('current_cats',)
    # autocomplete_fields = ['current_cats']

    list_filter = (
        'status',
        'prefers_kittens',
        'prefers_adults',
        'prefers_seniors',
        'prefers_medical_cases',
        'has_other_cats',
        'has_dogs',
        'has_children',
    )

    search_fields = (
        'full_name',
        'email',
        'phone_number',
        'city',
        'notes',
    )

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Fosterer Information', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone_number',
                'status',
            )
        }),
        ('Address', {
            'fields': (
                'address_line1',
                'address_line2',
                'city',
                'state',
                'postal_code',
            )
        }),
        ('Preferences', {
            'fields': (
                'prefers_kittens',
                'prefers_adults',
                'prefers_seniors',
                'prefers_medical_cases',
                'prefers_short_term',
                'prefers_long_term',
            ),
            'classes': ('collapse',)
        }),
        ('Household Information', {
            'fields': (
                'has_other_cats',
                'has_dogs',
                'has_children',
                'outdoor_space',
            ),
            'classes': ('collapse',)
        }),
        ('Internal Notes', {
            'fields': ('notes', 'created_at', 'updated_at', 'created_by'),
        }),
    )