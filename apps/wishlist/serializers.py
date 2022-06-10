from rest_framework import serializers
from apps.product.models import Product
from apps.product.serializers import ProductSerializer
from apps.wishlist.models import  WishListItem

class ProductSerializerWishnItem(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'price',
            'slug',
            'photo',
        ]


class WishListItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = WishListItem
        fields = [
            'id',
            'product',
        ]

