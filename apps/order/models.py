import uuid
from django.db import models
from apps.product.models import Product
from apps.order.Countries import Countries
from datetime import datetime
from django.contrib.auth import get_user_model
User = get_user_model()


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        not_processed = 'No Procesado'
        processed = 'Procesado'
        shipping = 'Enviado'
        delivered = 'Entregado'
        cancelled = 'Cancelado'

    status = models.CharField(
        max_length=50, choices=OrderStatus.choices, default=OrderStatus.not_processed)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=20)
    city = models.CharField(
        max_length=255, choices=Countries.choices, default=Countries.Lima)
    postal_zip_code = models.CharField(max_length=20)
    telephone_number = models.CharField(max_length=255)
    shipping_name = models.CharField(max_length=255)
    shipping_time = models.CharField(max_length=255)
    shipping_price = models.DecimalField(max_digits=7, decimal_places=2)
    date_issued = models.DateTimeField(auto_now_add=True)
    enterprise = models.CharField(max_length=255, default='')

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            year = datetime.now().year
            month = datetime.now().month
            date = datetime.now().day
            secont = datetime.now().second
            microsecond = datetime.now().microsecond
            count = Order.objects.filter(
                full_name=self.full_name, date_issued=self.date_issued, city=self.city).count() + 1
            total_count = "{0:04d}".format(count)
            self.transaction_id = "{}/{}-{}/{}-{}-{}/{}".format(
                year, self.full_name, self.city, month, date, total_count, secont, microsecond)

        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.transaction_id


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, related_name='products', on_delete=models.DO_NOTHING)
    order = models.ForeignKey(
        Order, related_name='orders', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    count = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['order', 'product']

    def __str__(self):
        return self.name
