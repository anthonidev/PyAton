from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions

from apps.wishlist.serializers import  WishListItemSerializer
from .models import WishList, WishListItem
from apps.product.models import Product
from apps.product.serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination


class WishListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = PageNumberPagination
    serializer_class = WishListItemSerializer
    queryset = WishListItem.objects.all()

    def list(self, request, format=None):
        user = self.request.user
        queryset = self.get_queryset()

        wishlist = WishList.objects.get(user=user)
        queryset = queryset.filter(wishlist=wishlist)
        serializer = self.serializer_class(
            queryset, many=True, context={'request': request})

        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)

    def post(self, request, format=None):
        user = self.request.user
        queryset = self.get_queryset()
        data = self.request.data
        wishlist = WishList.objects.get(user=user)
        try:
            product_id = int(data['product_id'])
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response(
                    {'error': 'This product does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            product = Product.objects.get(id=product_id)

            if WishListItem.objects.filter(wishlist=wishlist, product=product).exists():
                return Response(
                    {'error': 'Item already in wishlist'},
                    status=status.HTTP_409_CONFLICT
                )

            WishListItem.objects.create(
                product=product,
                wishlist=wishlist
            )
            queryset = queryset.filter(wishlist=wishlist)
            serializer = self.serializer_class(
                queryset, many=True, context={'request': request})

            page = self.paginate_queryset(serializer.data)
            return self.get_paginated_response(page)

        except:
            return Response(
                {'error': 'Something went wrong when adding item to wishlist'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, format=None):
        user = self.request.user
        queryset = self.get_queryset()
        wishlist = WishList.objects.get(user=user)
        try:
            product_id = request.query_params.get('product_id')
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            if not Product.objects.filter(id=product_id).exists():
                return Response(
                    {'error': 'Product with this ID does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            product = Product.objects.get(id=product_id)
            if not WishListItem.objects.filter(wishlist=wishlist, product=product).exists():
                return Response(
                    {'error': 'This product is not in your wishlist'},
                    status=status.HTTP_404_NOT_FOUND
                )
            WishListItem.objects.filter(
                wishlist=wishlist,
                product=product
            ).delete()

            queryset = queryset.filter(wishlist=wishlist)
            serializer = self.serializer_class(
                queryset, many=True, context={'request': request})

            page = self.paginate_queryset(serializer.data)
            return self.get_paginated_response(page)

        except:
            return Response(
                {'error': 'Something went wrong when removing wishlist item'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
