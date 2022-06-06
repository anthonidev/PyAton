from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from apps.order.Countries import Countries
from datetime import datetime

User = settings.AUTH_USER_MODEL


TREATMENT_OPTIONS = (
    ('Sr.', 'Sr.'),
    ('Sra.', 'Sra.'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    treatment = models.CharField(
        max_length=4, choices=TREATMENT_OPTIONS, default='Sr.')
    photo = CloudinaryField('Image', overwrite=True,
                            format="jpg", blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(default=datetime.now)
    dni = models.CharField(max_length=8, blank=True, null=True)
    def __str__(self):
        return self.user.first_name

class UserAddress(models.Model):
    account = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    enterprise = models.CharField(max_length=255, default='', blank=True, null=True)
    address = models.CharField(max_length=255, default='')
    zipcode = models.CharField(max_length=20, default='', blank=True, null=True)
    district = models.CharField(max_length=255, default='')
    city = models.CharField(
        max_length=255, choices=Countries.choices, default=Countries.Lima)
    phone = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.first_name
