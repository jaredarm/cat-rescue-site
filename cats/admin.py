from django.contrib import admin
from .models import Cat, CatImage, CatBreed
from django.utils.html import format_html

# Inline admin for CatImage
class CatImageInline(admin.TabularInline):
    model = CatImage
    extra = 1
    fields = ('image', 'caption', 'primary', 'preview',)
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 80px;" />', obj.image.url)
        return ""

# register cat breed model
@admin.register(CatBreed)
class CatBreedAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',) 

@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    inlines = [CatImageInline]

    list_display = (
        'name',
        'breed',
        'thumbnail',
        'status',
        'age',
        'colour',
        'sex',
        'id',
        'created_at',
    )

    list_filter = (
        'status',
        'breed',
        'colour',
        'sex',
        'created_at',
    )

    autocomplete_fields = ['bonded_cats',]

    search_fields = (
        'name',
        'breed',
        'breed_string',
        'description',
        'microchip_number'
    )

    ordering = ('-created_at',)

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Identification', {
            'fields': ('name', 'date_of_birth', 'estimated_dob', 'breed')
        }),
        ('Status', {
            'fields': ('status', 'fostered_in')
        }),
        ('Details', {
            'fields': ('tagline', 'description', 'colour', 'sex')
        }),
        ('Health', {
            'fields': (
                'is_vaccinated',
                'vaccinated_notes',
                'is_microchipped',
                'microchip_number',
                'is_sterilised',
                'is_fiv_positive',
                'health_notes',
            )
        }),
        ('Bonded Cats', {
            'fields': ('bonded_cats',)
        }),
        ('Compatibility', {
            'fields': (
                'is_good_with_kids',
                'good_with_kids_notes',
                'is_good_with_dogs',
                'good_with_dogs_notes',
                'is_good_with_cats',
                'good_with_cats_notes',
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail(self, obj):
        primary = obj.images.filter(primary=True).first()
        if not primary:
            primary = obj.images.first()

        if primary and primary.image:
            return format_html('<img src="{}" style="height: 60px;" />', primary.image.url)

        return ""

