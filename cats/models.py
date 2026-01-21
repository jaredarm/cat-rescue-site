from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Cat(models.Model):
    # Cat status choices
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending Adoption'),
        ('adopted', 'Adopted'),
        ('hold', 'On Hold'),
    ]
    # Cat sex choices
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    ]

    # Basic information
    name = models.CharField(max_length=100)   
    date_of_birth = models.DateField(null=True, blank=True)
    estimated_dob = models.BooleanField(default=False)
    breed = models.ForeignKey(
        'CatBreed',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    fostered_in = models.CharField(max_length=100, blank=True)

    # Additional details
    colour = models.CharField(max_length=100, blank=True)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    # Health and compatibility
    is_vaccinated = models.BooleanField(default=False)
    vaccinated_notes = models.CharField(blank=True)
    
    is_microchipped = models.BooleanField(default=False)
    microchip_number = models.CharField(max_length=50, blank=True)

    is_sterilised = models.BooleanField(default=False)
    
    is_fiv_positive = models.BooleanField(default=False)
    health_notes = models.CharField(blank=True)

    is_good_with_kids = models.BooleanField(default=False)
    good_with_kids_notes = models.CharField(blank=True)

    is_good_with_dogs = models.BooleanField(default=False)
    good_with_dogs_notes = models.CharField(blank=True)

    is_good_with_cats = models.BooleanField(default=False)
    good_with_cats_notes = models.CharField(blank=True)

    # Sex
    sex = models.CharField(
        max_length=20, 
        choices=SEX_CHOICES,
        default='unknown'
    )

    # Bonded cats
    bonded_cats = models.ManyToManyField(
        'self',
        symmetrical=True,
        blank=True
    )

    # Admin + internal notes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cats_created'
    )

    # Calculate age in years and months
    @property
    def age(self):
        if not self.date_of_birth:
            return "Unknown"

        today = date.today()
        dob = self.date_of_birth

        # Calculate years
        years = today.year - dob.year
        if (today.month, today.day) < (dob.month, dob.day):
            years -= 1

        # Calculate months
        months = today.month - dob.month
        if today.day < dob.day:
            months -= 1
        if months < 0:
            months += 12

        # Build the base age string
        parts = []
        if years > 0:
            parts.append(f"{years} year{'s' if years != 1 else ''}")
        if months > 0:
            parts.append(f"{months} month{'s' if months != 1 else ''}")

        age_str = ", ".join(parts) if parts else "0 months"

        # Add estimated tag
        # if self.estimated_dob:
        #     age_str += " (estimated)"

        return age_str

    # Primary image, returns the primary CatImage if exists
    @property
    def primary_image(self):
        return self.images.filter(primary=True).first()

    # String representation
    def __str__(self):
        return self.name

# Additional model for Cat Images
class CatImage(models.Model):
    cat = models.ForeignKey('Cat', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cats/')
    caption = models.CharField(max_length=200, blank=True)
    primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.cat.name}"
    
    def save(self, *args, **kwargs):
        # If this image is marked primary, unset all others for the same cat
        if self.primary:
            CatImage.objects.filter(cat=self.cat, primary=True).exclude(id=self.id).update(primary=False)
        super().save(*args, **kwargs)

# Additional model for Cat Breed
class CatBreed(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name