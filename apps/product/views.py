import random
from .models import Brand, Category, CharacteristicProduct, Product, ProductImage
from .serializers import (
    BrandSerializer,
    CategoryChildrenSerializer,
    CategorySerializer,
    CharacteristicProductSerializer,
    DetailProductSerializer,
    ProductImageSerializer,
    ProductSerializer
)
from rest_framework import status, permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from datetime import datetime


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = DetailProductSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = None

    def get(self, request, slug, *args, **kwargs):
        if Product.objects.filter(slug=slug).exists():
            product = Product.objects.get(slug=slug)
            Product.objects.filter(slug=slug).update(
                num_visits=product.num_visits + 1, last_visit=datetime.now())
            serializer = self.serializer_class(product)

            return Response({'detail_product': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Product with this ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)


class ProductDetailViewa(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    pagination_class = None
    serializer_class = ProductSerializer

    def get(self, request, slug, format=None):
        if Product.objects.filter(slug=slug).exists():
            product = Product.objects.get(slug=slug)

            related_products = product.category.categories.filter(
                parent=None).order_by("?").exclude(id=product.id)

            if product.variants.all():
                products_colors = list(
                    product.variants.all().exclude(id=product.id))
            elif product.parent:
                products_colors = list(
                    product.parent.variants.all().exclude(id=product.id))
                related_products = list(product.category.products.filter(
                    parent=None).exclude(id=product.parent.id))

                products_colors.append(product.parent)
            else:
                products_colors = []

            Product.objects.filter(slug=slug).update(
                num_visits=product.num_visits + 1,
                last_visit=datetime.now(),
            )
            characteristic = []
            images = []
            if CharacteristicProduct.objects.filter(product=product).exists():
                characteristic = CharacteristicProduct.objects.filter(
                    product=product)
            if ProductImage.objects.filter(product=product).exists():
                images = ProductImage.objects.filter(product=product)

            characteristic = CharacteristicProductSerializer(
                characteristic, many=True)
            images = ProductImageSerializer(images, many=True)
            products_views = list(Product.objects.order_by(
                '-num_visits').exclude(id=product.id).exclude(id__in=related_products))[:10]
            products_views = random.sample(products_views, 4)

            return Response({
                'characteristic': characteristic.data,
                'images': images.data,
                'related': self.serializer_class(related_products, many=True).data[:4],
                'products_views': self.serializer_class(products_views, many=True).data,
                'colors': self.serializer_class(products_colors, many=True).data,
                'product': self.serializer_class(product).data,
            }, status=status.HTTP_200_OK)

        else:
            return Response(
                {'error': 'Product with this ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)


class ListBrandView(generics.ListAPIView):
    serializer_class = BrandSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = None
    queryset = Brand.objects.all()

    def list(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = BrandSerializer(queryset, many=True)
        return Response({'brands': serializer.data}, status=status.HTTP_200_OK)


class ListCategoryView(generics.ListAPIView):
    pagination_class = None
    permission_classes = (permissions.AllowAny, )
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(parent=None)

    def list(self, request, format=None, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListProductsHomeView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def list(self, request, format=None):
        queryset = self.get_queryset()
        products_featured = queryset.filter(is_featured=True)
        products_news = queryset.order_by('-date_added')
        products_views = queryset.order_by('-num_visits')
        products_sold = queryset.order_by('-sold')

        if products_featured and products_news and products_views and products_sold:
            products_featured = self.serializer_class(
                products_featured, many=True, context={"request": request})

            products_news = self.serializer_class(
                products_news, many=True, context={"request": request})

            products_views = self.serializer_class(
                products_views, many=True, context={"request": request})

            products_sold = self.serializer_class(
                products_sold, many=True, context={"request": request})

            return Response(
                {'home': {
                    'products_featured': products_featured.data[:6],
                    'products_news': products_news.data[:6],
                    'products_views': products_views.data[:6],
                    'products_sold': products_sold.data[:6]
                }
                }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'No products to list'},
                status=status.HTTP_404_NOT_FOUND)


class ListProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny, )


class ListBySearchView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny, )
    queryset = Product.objects.all()

    def post(self, request, format=None, *args, **kwargs):
        data = self.request.data
        queryset = self.get_queryset()

        categories = data['categories']
        brands = data['brands']
        order = data['order']
        sort_by = data['sort_by']
        price_range = data['price_range']
        query = data['query']

        if len(query) > 0:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query))

        if len(categories) != 0:
            filtered_categories = []
            for cat in categories:
                filtered_categories.append(cat)

            queryset = queryset.filter(
                category__in=filtered_categories)

        if len(brands) != 0:
            filtered_brands = []
            for brand in brands:
                filtered_brands.append(brand)
            queryset = queryset.filter(brand__in=filtered_brands)

        if not (sort_by == 'date_added' or sort_by == 'price' or sort_by == 'sold' or sort_by == 'name'):
            sort_by = 'date_added'

        if order == 'desc':
            sort_by = '-' + sort_by
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by(sort_by)

         # Filtrar por precio
        if price_range == '1 - 50':
            queryset = queryset.filter(price__gte=1)
            queryset = queryset.filter(price__lt=51)
        elif price_range == '51 - 70':
            queryset = queryset.filter(price__gte=51)
            queryset = queryset.filter(price__lt=71)
        elif price_range == '71 - 90':
            queryset = queryset.filter(price__gte=71)
            queryset = queryset.filter(price__lt=91)
        elif price_range == '91 - 119':
            queryset = queryset.filter(price__gte=91)
            queryset = queryset.filter(price__lt=120)
        elif price_range == 'Más de 120':
            queryset = queryset.filter(price__gte=120)

        serializer = self.serializer_class(queryset, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


class ProductsCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny, )
    queryset = Product.objects.all()

    def get(self, request, slug, format=None, *args, **kwargs):
        queryset = self.get_queryset()

        if Category.objects.filter(slug=slug).exists():
            category = Category.objects.get(slug=slug)
            if not category.parent:
                filtered_categories = Category.objects.filter(parent=category)
                queryset = queryset.filter(
                    category__in=filtered_categories)
            else:
                queryset = queryset.filter(
                    category=category)

            page = self.paginate_queryset(queryset)
            if queryset and page is not None:
                return self.get_paginated_response(self.serializer_class(queryset, many=True).data)
            return Response('Not found', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                {'error': 'Category with this ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)


class BrandsCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny, )
    queryset = Product.objects.all()

    def get(self, request, id, format=None, *args, **kwargs):
        queryset = self.get_queryset()
        if Brand.objects.filter(id=id).exists():
            brand = Brand.objects.get(id=id)
            queryset = queryset.filter(
                brand=brand)

            page = self.paginate_queryset(queryset)
            if queryset and page is not None:
                return self.get_paginated_response(self.serializer_class(queryset, many=True).data)
            return Response('Not found', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                {'error': 'Category with this ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)


class GetSubCategoryView(generics.ListAPIView):
    serializer_class = CategoryChildrenSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny, )
    queryset = Category.objects.all()

    def get(self, request, slug, format=None, *args, **kwargs):
        if Category.objects.filter(slug=slug).exists():
            self.queryset = self.queryset.get(slug=slug)
            return Response(self.serializer_class(self.queryset).data)
        else:
            return Response(
                {'error': 'Category with this ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)
