from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions

from .models import Cart, CartItem

from apps.product.models import Product
from apps.product.serializers import ProductSerializer
from .serializers import CartSerializer


class CartView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = None
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def list(self, request, format=None):
        user = self.request.user
        queryset = self.get_queryset()
        return Response(
            {'cart': self.serializer_class(queryset.get(user=user)).data},
            status=status.HTTP_200_OK
        )

    def post(self, request, format=None):
        user = self.request.user
        queryset = self.get_queryset()
        data = self.request.data
        try:
            product_id = int(data['product_id'])
        except:
            return Response({'error': 'Product ID must be an integer'}, status=status.HTTP_404_NOT_FOUND)
        count = 1

        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response({'error': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)

            product = Product.objects.get(id=product_id)
            queryset = queryset.get(user=user)
            if CartItem.objects.filter(cart=queryset, product=product).exists():
                return Response({'error': 'Producto already in cart'}, status=status.HTTP_423_LOCKED)

            if int(product.quantity) >= count:
                CartItem.objects.create(
                    product=product,
                    cart=queryset,
                    count=count
                )
                return Response(
                    {'cart': self.serializer_class(queryset).data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({'error': 'Not enough of this item in stock'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Something went wrong when adding item to cart'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        user = self.request.user
        queryset = self.get_queryset()
        data = self.request.data
        try:
            product_id = int(data['product_id'])
            count = int(data['count'])
        except:
            return Response({'error': ' productID or count must be an integer'}, status=status.HTTP_404_NOT_FOUND)
        queryset = queryset.get(user=user)
        product = Product.objects.get(id=product_id)
        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response({'error': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)
            if CartItem.objects.filter(cart=queryset, product=product).exists():
                if(int(product.quantity) >= count):
                    CartItem.objects.filter(
                        cart=queryset, product=product).update(count=count)
                else:
                    return Response({'error': 'Not enough of this item in stock'}, status=status.HTTP_423_LOCKED)

                return Response(
                    {'cart': self.serializer_class(queryset).data},
                    status=status.HTTP_200_OK
                )

            else:
                return Response({'error': 'Producto not exist in cart'}, status=status.HTTP_423_LOCKED)

        except:
            return Response({'error': 'Something went wrong when update item to cart'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        user = self.request.user
        queryset = self.get_queryset()
        product_id = request.query_params.get('id')

        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)
            if CartItem.objects.filter(product=product).exists():
                CartItem.objects.filter(product=product_id).delete()
                queryset = queryset.get(user=user)
                return Response(
                    {'cart': self.serializer_class(queryset).data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({'error': 'Producto not exist in cart'}, status=status.HTTP_423_LOCKED)
        else:
            return Response({'error': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)


class EmptyCartView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = None
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def delete(self, request, format=None):
        user = self.request.user
        queryset = self.get_queryset()

        try:
            queryset = queryset.get(user=user)
            if not CartItem.objects.filter(cart=queryset).exists():
                return Response({'success': 'Cart is already empty'}, status=status.HTTP_200_OK)

            CartItem.objects.filter(cart=queryset).delete()

            return Response(
                {'cart': self.serializer_class(queryset).data},
                status=status.HTTP_200_OK
            )
        except:
            return Response({'error': 'Something went wrong emptying cart'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SynchCartView(APIView):
    def put(self, request, format=None):
        user = self.request.user
        data = self.request.data
        print(user)

        try:
            cart_items = data['cart_items']
            for cart_item in cart_items:
                cart = Cart.objects.get(user=user)
                try:
                    product_id = int(cart_item['product_id'])
                except:
                    return Response({'error': 'Product ID must be an integer'}, status=status.HTTP_404_NOT_FOUND)

                if not Product.objects.filter(id=product_id).exists():
                    return Response({'error': 'Product with this ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

                product = Product.objects.get(id=product_id)
                quantity = product.quantity

                if CartItem.objects.filter(cart=cart, product=product).exists():
                    # Actualiizamos el item del carrito
                    item = CartItem.objects.get(cart=cart, product=product)
                    count = item.count

                    try:
                        cart_item_count = int(cart_item['count'])
                    except:
                        cart_item_count = 1

                    # Chqueo con base de datos
                    if (cart_item_count + int(count)) <= int(quantity):
                        updated_count = cart_item_count + int(count)
                        CartItem.objects.filter(
                            cart=cart, product=product).update(count=updated_count)
                else:
                    # Agregar el item al carrito del usuario
                    try:
                        cart_item_count = int(cart_item['count'])
                    except:
                        cart_item_count = 1

                    if cart_item_count <= quantity:
                        CartItem.objects.create(
                            product=product, cart=cart, count=cart_item_count)

                        if CartItem.objects.filter(cart=cart, product=product).exists():
                            # Sumar item
                            total_items = int(cart.total_items) + 1
                            Cart.objects.filter(user=user).update(
                                total_items=total_items)

            return Response({'success': 'Cart Synchronized'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Something went wrong when synching cart'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
