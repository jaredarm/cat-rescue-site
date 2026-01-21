from django.db import models
from django.contrib.auth.models import User

class FosterHome(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending Approval'),
    ]

    # Basic information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Address details
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    # Foster home preferences
    prefers_kittens = models.BooleanField(default=False)
    prefers_adults = models.BooleanField(default=False)
    prefers_seniors = models.BooleanField(default=False)
    prefers_medical_cases = models.BooleanField(default=False)
    prefers_short_term = models.BooleanField(default=False)
    prefers_long_term = models.BooleanField(default=False)
    max_cats = models.PositiveIntegerField(default=1)
    
    # Household details
    has_other_cats = models.BooleanField(default=False)
    has_dogs = models.BooleanField(default=False)
    has_children = models.BooleanField(default=False)
    outdoor_space = models.BooleanField(default=False)

    # Admin + internal notes
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fosterhome_created'
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name
