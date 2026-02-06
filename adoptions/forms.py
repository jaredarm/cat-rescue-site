from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ["status", "submitted_at", "reviewed_at", "reviewer"]

        widgets = {
            "cats": forms.SelectMultiple(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            }),
            "reason_for_adopting": forms.Textarea(attrs={
                "rows": 3,
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            }),
            "how_found_cat": forms.Select(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            }),

            # Contact fields
            "first_name": forms.TextInput(attrs={"class": "input"}),
            "family_name": forms.TextInput(attrs={"class": "input"}),
            "address_line1": forms.TextInput(attrs={"class": "input"}),
            "address_line2": forms.TextInput(attrs={"class": "input"}),
            "city": forms.TextInput(attrs={"class": "input"}),
            "state": forms.TextInput(attrs={"class": "input"}),
            "postal_code": forms.TextInput(attrs={"class": "input"}),
            "country": forms.TextInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
            "phone": forms.TextInput(attrs={"class": "input"}),
            "occupation": forms.TextInput(attrs={"class": "input"}),

            # Household
            "accommodation_type": forms.Select(attrs={"class": "input"}),
            "children_and_ages": forms.TextInput(attrs={"class": "input"}),
            "hours_alone": forms.TextInput(attrs={"class": "input"}),
            "home_photos": forms.ClearableFileInput(attrs={"class": "input"}),
            "home_additional_info": forms.Textarea(attrs={"class": "textarea"}),

            # Other pets
            "other_pet_behaviour": forms.Textarea(attrs={"class": "textarea"}),
            "other_pet_additional_info": forms.Textarea(attrs={"class": "textarea"}),

            # Experience
            "previous_cat_experience": forms.Textarea(attrs={"class": "textarea"}),
            "medical_care_plan": forms.Textarea(attrs={"class": "textarea"}),
            "lost_cat_plan": forms.Textarea(attrs={"class": "textarea"}),
            "diet_plan": forms.Textarea(attrs={"class": "textarea"}),
            "surrendered_animals_history": forms.Textarea(attrs={"class": "textarea"}),
            "adoption_refusal_history": forms.Textarea(attrs={"class": "textarea"}),
        }