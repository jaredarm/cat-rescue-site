from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "get_cats",
        "status",
        "submitted_at",
        "reviewer",
    )
    list_filter = ("status", "submitted_at", "reviewer", "cats")
    search_fields = ("first_name", "family_name", "email")
    ordering = ("-submitted_at",)

    readonly_fields = ("submitted_at", "reviewed_at")

    autocomplete_fields = ("cats",)

    fieldsets = (
        ("Cats Details", {
            "fields": ("cats", "reason_for_adopting", "how_found_cat")
        }),
        ("Applicant Info", {
            "fields": ("first_name", "family_name", "address_line1", "address_line2", "city", "state", "postal_code", "country", "email", "phone", "occupation")
        }),
        ("Household", {
            "fields": ("accommodation_type", "busy_street", "allergies", "number_of_people", "children_and_ages", "hours_alone", "home_photos", "home_additional_info")
        }),
        ("Other pets", {
            "fields": ("other_pets_cat", "other_pets_dog", "other_pets_rabbit", "other_pets_other", "other_pets_microchipped", "other_pets_sterilised", "other_pets_vaccinated", "other_pet_behaviour", "other_pet_additional_info")
        }),
        ("Previous experience", {
            "fields": ("previous_cat_experience", "medical_care_plan", "lost_cat_plan", "diet_plan", "surrendered_animals_history", "adoption_refusal_history")
        }),
        ("Declarations", {
            "fields": ("indoor_only", "can_afford_care", "will_return_if_needed")
        }),
        ("Review Workflow", {
            "fields": ("status", "reviewer", "reviewed_at")
        }),
    )

    def get_cats(self, obj):
        return ", ".join(cat.name for cat in obj.cats.all())
    get_cats.short_description = "Cats"
    