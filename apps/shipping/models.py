from django.db import models
from cloudinary.models import CloudinaryField


class Shipping(models.Model):
    class Meta:
        verbose_name = 'Shipping'
        verbose_name_plural = 'Shipping'
    photo = CloudinaryField('Image', overwrite=True,
                            format="jpg", blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    time_to_delivery = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name