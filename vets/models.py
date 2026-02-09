from django.db import models


class Vet(models.Model):
    name = models.CharField(max_length=255)
    # Address
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    logo = models.FileField(
        upload_to="vets/logos/", blank=True
    )
    website = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50)
