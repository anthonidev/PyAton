from rest_framework import serializers
from .models import  Category, CharacteristicProduct, Product, Brand, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        
        fields = [
            'id',
            'title',
            'is_featured',
            'photo',
            'slug',
            'description',
            'get_parent',
            'get_parent_slug',
        ]



class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id',
            'title',
        ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'get_category',
            'get_brand',
            'title',
            'price',
            'compare_price',
            'is_featured',
            'quantity',
            'date_added',
            'slug',
            'num_visits',
            'last_visit',
            'sold',
            'photo',
            'get_absolute_url',
            'description'
        ]
        
        
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = [
#             'id',
#             'get_category',
#             'title',
#             'price',
#             'compare_price',
#             'photo',
#             'slug',
#             'quantity',
#         ]
class CharacteristicProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacteristicProduct
        
        fields = [
            'title',
        ]
class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductImage
        fields = [
            'id',
            'photo',
        ]
