from apps.order.models import Order,OrderItem
from rest_framework import serializers
from apps.product.models import Product

class ProductSerializerOrdernItem(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'price',
            'slug',
            'photo',
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    product=ProductSerializerOrdernItem()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'count', 'date_added',]


class OrderSerializer(serializers.ModelSerializer):
    orders = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'transaction_id',
            'amount',
            'full_name',
            'address',
            'district',
            'city',
            'postal_zip_code',
            'date_issued',
            'orders',
        ]
