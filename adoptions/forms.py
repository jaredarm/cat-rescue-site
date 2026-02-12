from django import forms
from .models import Application
from common.forms import TailwindModelForm


class ToggleWidget(forms.CheckboxInput):
    template_name = "adoptions/widgets/toggle_widget.html"


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
            "how_found_cat": "How did you find your chosen cat?",

            # Personal / contact
            "first_name": "First name",
            "family_name": "Last name",
            "address_line1": "Street address",
            "address_line2": "Street address (line 2)",
            "city": "City",
            "state": "State / Province",
            "postal_code": "Postal / Zip Code",
            "country": "Country",
            "email": "Email",
            "phone": "Phone number",
            "occupation": "Occupation",
            "vet_name": "Do you have an existing vet or vet in mind for your new addition? If so, please provide the vet's name",
            "driving_license": "Please provide a picture of your driving licence so we can verify your address",

            # Household
            "accommodation_type": "What type of accommodation do you live in?",
            "busy_street": "Do you live on a busy street?",
            "allergies": "Is anyone in your home allergic to cats?",
            "number_of_people": "How many people live in your home?",
            "children_and_ages": "How many children live in your home and what are their ages?",
            "hours_alone": "How many hours will the cat be left on its own each day?",
            "home_photos": "Please provide photos of the areas a kitty will be living in so we can see it is a safe environment for one of our cats",
            "home_additional_info": "Is there anything else you would like to tell us about your home?",

            # Other pets
            "other_pets_cat": "Do you have other cats?",
            "other_pets_dog": "Do you have other dogs?",
            "other_pets_rabbit": "Do you have other rabbits?",
            "other_pets_other": "Do you have other types of pets?",
            "other_pets_microchipped": "Are your other pets microchipped?",
            "other_pets_sterilised": "Are your other pets sterilised?",
            "other_pets_vaccinated": "Are your other pets vaccinated?",
            "other_pet_behaviour": "Do your animals have any behavioural problems?",
            "other_pet_additional_info": "Is there anything else you would like to tell us about your other pets?",

            # Experience & plans
            "previous_cat_experience": "Have you previously shared your life with a cat?",
            "medical_care_plan": "Should your cat become ill or injured and require expensive medical care, what would be your course of action?",
            "lost_cat_plan": "If your cat got lost what would you do?",
            "diet_plan": "Will you provide a stable diet to your cat? If so, please provide more information",
            "surrendered_animals_history": "Have you ever taken an animal to a shelter or released it to another party? If so, please provide more information here",
            "adoption_refusal_history": "Have you ever been refused adoption of an animal? If so, please provide more information here",

            # Declarations
            "indoor_only": "I confirm that my cat will be kept indoors, in a secure cat run or on a cat harness at all times to protect it from harm or injury",
            "can_afford_care": "I confirm I am able to afford the ongoing cost of owning a cat and am prepared to continue with the cat's vaccinations, flea and worm treatments as required?",
            "will_return_if_needed": "I agree to return the cat or cats to 9 Lives Cat Rescue should my circumstances change and I can no longer care for the animal?",
        }
        fieldsets = (
            ('Cat Details', {
                'description': 'Select the cat(s) you are applying for and provide brief details about them.',
                'fields': ('cats', 'reason_for_adopting', 'how_found_cat', 'vet_name', 'driving_license')
            }),
            ('Personal Information', {
                'description': 'Your contact details so we can get in touch about your application.',
                'fields': ('first_name', 'family_name', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'email', 'phone', 'occupation')
            }),
            ('Household', {
                'description': 'Information about who lives in the home and the environment the cat will live in.',
                'fields': ('accommodation_type', 'busy_street', 'allergies', 'number_of_people', 'children_and_ages', 'hours_alone', 'home_photos', 'home_additional_info')
            }),
            ('Other Pets', {
                'description': 'Tell us about other pets you may already have.',
                'fields': ('other_pets_cat', 'other_pets_dog', 'other_pets_rabbit', 'other_pets_other', 'other_pets_microchipped', 'other_pets_sterilised', 'other_pets_vaccinated', 'other_pet_behaviour', 'other_pet_additional_info')
            }),
            ('Experience & Plans', {
                'description': 'Questions about your previous experience and plans for the cat.',
                'fields': ('previous_cat_experience', 'medical_care_plan', 'lost_cat_plan', 'diet_plan', 'surrendered_animals_history', 'adoption_refusal_history')
            }),
            ('Declarations', {
                'description': 'Please confirm the following declarations.',
                'fields': ('indoor_only', 'can_afford_care', 'will_return_if_needed')
            }),
        )
        widgets = {
            "reason_for_adopting": forms.Textarea(attrs={
                "rows": 3,
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            }),
            "how_found_cat": forms.Select(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # expose fieldsets on the form instance for templates
        self.fieldsets = getattr(self.Meta, 'fieldsets', ())
        # render boolean-style fields as toggle switches
        bool_fields = [
            'busy_street', 'allergies',
            'other_pets_cat', 'other_pets_dog', 'other_pets_rabbit', 'other_pets_other',
            'other_pets_microchipped', 'other_pets_sterilised', 'other_pets_vaccinated',
            'indoor_only', 'can_afford_care', 'will_return_if_needed'
        ]

        for name in bool_fields:
            if name in self.fields:
                self.fields[name].widget = ToggleWidget()
        # expose a simple widget type name on each field to make template logic safer
        for name, field in self.fields.items():
            try:
                field.widget_type = field.widget.__class__.__name__
            except Exception:
                field.widget_type = ''
