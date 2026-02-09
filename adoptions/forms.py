from django import forms
from .models import Application
from core.forms import TailwindModelForm


class ApplicationForm(TailwindModelForm):
    class Meta:
        model = Application
        exclude = (
            "status",
            "submitted_at",
            "reviewed_at",
            "reviewer"
        )
        labels = {
            "cats": "Please select the cat(s) you are interested in adopting",
            "reason_for_adopting": "Why would you like to adopt your chosen cat or cats?",
            "how_found_cat": "How did you find your chosen cat?"
        }
        fieldsets = (
            ('Personal Information', {
             'fields': ('first_name', 'family_name', 'address_line1', 'address_line2', 'city')}),
        )
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
        }
