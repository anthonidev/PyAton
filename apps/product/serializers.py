from rest_framework import serializers
from .models import Category, CharacteristicProduct, Product, Brand, ProductImage


class CharacteristicProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacteristicProduct

        fields = [
            'title',
            'description',
        ]


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = [
            'id',
            'photo',
            'photo_thumbnail_sm',
            'photo_thumbnail_xm',
        ]


class ColorProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'price',
            'compare_price',
            'photo',
            'photo_thumbnail_sm',
            'photo_thumbnail_xm',
            'slug',
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
            'sold',
            'photo',
            'photo_thumbnail_sm',
            'photo_thumbnail_xm',
            'description'
        ]


class DetailProductSerializer(serializers.ModelSerializer):
    characteristics = CharacteristicProductSerializer(many=True)
    images = ProductImageSerializer(many=True)
    colors = ProductSerializer(many=True, source="get_colors")
    related = ProductSerializer(many=True, source="related_products")

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
            'slug',
            'sold',
            'photo',
            'photo_thumbnail_sm',
            'photo_thumbnail_xm',
            'description',
            'characteristics',
            'images',
            'colors',
            'related'
        ]


class CategoryChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'slug',
            'get_parent',
            'get_parent_slug',
            'get_total'
        ]


class CategorySerializer(serializers.ModelSerializer):
    children = CategoryChildrenSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'photo',
            'slug',
            'children',
        ]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id',
            'title',
        ]

