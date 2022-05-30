from django.db import models
from apps.product.models import Product
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Cart(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    total_items=models.IntegerField(default=0)
    def __str__(self):
        return  self.user.email

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE )
    count = models.IntegerField()
    def __str__(self):
        return  self.product.title