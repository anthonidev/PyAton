from apps.product.models import Product
from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL


class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name


class WishListItem(models.Model):
    wishlist = models.ForeignKey(
        WishList, related_name='wish', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='items', on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ['wishlist', 'product']

    def __str__(self):
        return self.product.title
