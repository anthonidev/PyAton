from django.db import models
from apps.product.models import Product
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

    def get_amount(self):
        amount = 0
        items = CartItem.objects.filter(cart=self)
        for item in items:
            amount += item.get_total()
        return round(amount, 2)

    def get_total_items(self):
        return CartItem.objects.filter(cart=self).count()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()

    class Meta:
        ordering = ('-id',)
    
    def __str__(self):
        return self.product.title

    def get_total(self):
        return self.product.price * self.count
