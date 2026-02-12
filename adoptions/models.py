from django.db import models


class Application(models.Model):
    FIND_US_CHOICES = [
        ('9liveswebsite', '9 Lives website'),
        ('9livesfoster', '9 Lives foster carer'),
        ('facebook', 'Facebook'),
        ('gumtree', 'Gumtree'),
        ('instagram', 'Instagram'),
        ('friendfamily', 'Friend or family member'),
        ('other', 'Other'),
    ]

    APPLICATION_STATUS = [
        ('submitted', 'Submitted'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]

    ACCOMMODATION_CHOICES = [
        ("home_owner", "Home owner"),
        ("renting", "Renting on your own or with a partner"),
        ("house_share", "House sharing"),
        ("other", "Other"),
    ]

    # Cat details
    cats = models.ManyToManyField(
        "cats.Cat", related_name="applications", blank=True)
    reason_for_adopting = models.TextField(blank=True)
    how_found_cat = models.CharField(
        max_length=50, choices=FIND_US_CHOICES, blank=True
    )

    # Contact details
    first_name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255)

    # Address details
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=50)
    occupation = models.CharField(max_length=100, blank=True)
    # Vet details
    vet_name = models.CharField(max_length=255, blank=True)
    # Driving licence upload for address verification
    driving_license = models.FileField(upload_to='applications/driving_licenses/', blank=True)

    # Household
    accommodation_type = models.CharField(
        max_length=50, choices=ACCOMMODATION_CHOICES, blank=True
    )
    busy_street = models.BooleanField(default=False)
    allergies = models.BooleanField(default=False)
    number_of_people = models.PositiveIntegerField(default=1)
    children_and_ages = models.CharField(max_length=255, blank=True)
    hours_alone = models.CharField(max_length=100, blank=True)
    home_photos = models.FileField(
        upload_to="applications/home_photos/", blank=True
    )
    home_additional_info = models.TextField(blank=True)

    # Other pets
    other_pets_cat = models.BooleanField(default=False)
    other_pets_dog = models.BooleanField(default=False)
    other_pets_rabbit = models.BooleanField(default=False)
    other_pets_other = models.BooleanField(default=False)

    other_pets_microchipped = models.BooleanField(default=False)
    other_pets_sterilised = models.BooleanField(default=False)
    other_pets_vaccinated = models.BooleanField(default=False)

    other_pet_behaviour = models.TextField(blank=True)
    other_pet_additional_info = models.TextField(blank=True)

    # Previous experience
    previous_cat_experience = models.TextField(blank=True)
    medical_care_plan = models.TextField(blank=True)
    lost_cat_plan = models.TextField(blank=True)
    diet_plan = models.TextField(blank=True)
    surrendered_animals_history = models.TextField(blank=True)
    adoption_refusal_history = models.TextField(blank=True)

    # Declarations
    indoor_only = models.BooleanField(default=False)
    can_afford_care = models.BooleanField(default=False)
    will_return_if_needed = models.BooleanField(default=False)

    # Meta
    status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS,
        default='submitted',
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewer = models.ForeignKey(
        "auth.User", null=True, blank=True, on_delete=models.SET_NULL
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.family_name}"

    def __str__(self):
        return f"{self.first_name} {self.family_name}"
