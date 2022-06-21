from math import e
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.account.models import UserAddress, UserProfile
from apps.cart.models import Cart, CartItem
from apps.coupon.models import Coupon
from apps.order.models import Order, OrderItem
from apps.order.serializers import OrderSerializer
from apps.product.models import Product
from apps.shipping.models import Shipping
from rest_framework import status, generics, permissions
from rest_framework.pagination import PageNumberPagination
from django.core.mail import send_mail


class OrderView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = PageNumberPagination
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def list(self, request, format=None):
        user = self.request.user
        queryset = self.get_queryset()

        queryset = queryset.filter(user=user)
        serializer = self.serializer_class(
            queryset, many=True, context={'request': request})
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


class GetOrderTotalView(APIView):
    def get(self, request, format=None):
        user = self.request.user
        shipping_id = request.query_params.get('shipping_id')
        shipping_id = str(shipping_id)

        coupon_code = request.query_params.get('coupon_code')
        coupon_code = str(coupon_code)

        try:
            cart = Cart.objects.get(user=user)

            # revisar si existen iitems
            if not CartItem.objects.filter(cart=cart).exists():
                return Response(
                    {'error': 'Need to have items in cart'},
                    status=status.HTTP_404_NOT_FOUND
                )

            cart_items = CartItem.objects.filter(cart=cart)

            for cart_item in cart_items:
                if not Product.objects.filter(id=cart_item.product.id).exists():
                    return Response(
                        {'error': 'A proudct with ID provided does not exist'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                if int(cart_item.count) > int(cart_item.product.quantity):
                    return Response(
                        {'error': 'Not enough items in stock'},
                        status=status.HTTP_200_OK
                    )

                total_amount = 0.0
                total_after_coupon = 0.0
                for cart_item in cart_items:
                    total_amount += (float(cart_item.product.price)
                                     * float(cart_item.count))

                original_price = round(total_amount, 2)
                # Cupones
                if coupon_code != '' and coupon_code != 'default':
                    # Revisar si cupon de precio fijo es valido
                    if Coupon.objects.filter(code__iexact=coupon_code).exists():
                        price_coupon = Coupon.objects.get(code=coupon_code)

                    discount_amount = float(price_coupon.value)
                    if discount_amount < total_amount:
                        total_amount -= discount_amount
                        total_after_coupon = total_amount

                # Total despues del cupon
                total_after_coupon = round(total_after_coupon, 2)

                # total_amount += (total_amount * tax)

                shipping_cost = 0.0

                # verificar que el envio sea valido
                if Shipping.objects.filter(id__iexact=shipping_id).exists():
                    # agregar shipping a total amount
                    shipping = Shipping.objects.get(id=shipping_id)
                    shipping_cost = shipping.price
                    total_amount += float(shipping_cost)

                total_amount = round(total_amount, 2)

                return Response({
                    'original_price': f'{original_price:.2f}',
                    'total_after_coupon': f'{total_after_coupon:.2f}',
                    'total_amount': f'{total_amount:.2f}',
                    'shipping_cost': f'{shipping_cost:.2f}'
                },
                    status=status.HTTP_200_OK
                )

        except:
            return Response(
                {'error': 'Something went wrong when retrieving payment total information'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProcessOrderView(APIView):
    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data

        shipping_id = str(data['shipping_id'])
        coupon_code = str(data['coupon_code'])
        address_id = str(data['address_id'])

        user_profile = UserProfile.objects.get(user=user)
        addressObject = UserAddress.objects.get(
            account=user_profile, id=address_id)

        if(addressObject):
            full_name = addressObject.first_name + " " + addressObject.last_name
            address = addressObject.address
            city = addressObject.city
            district = addressObject.district
            postal_zip_code = addressObject.zipcode
            telephone_number = addressObject.phone
        else:
            return Response(
                {'error': 'Address does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        if not Shipping.objects.filter(id__iexact=shipping_id).exists():
            return Response(
                {'error': 'Invalid shipping option'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart = Cart.objects.get(user=user)

        # revisar si usuario tiene items en carrito
        if not CartItem.objects.filter(cart=cart).exists():
            return Response(
                {'error': 'Need to have items in cart'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_items = CartItem.objects.filter(cart=cart)

        for cart_item in cart_items:
            if not Product.objects.filter(id=cart_item.product.id).exists():
                return Response(
                    {'error': 'Transaction failed, a proudct ID does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
            if int(cart_item.count) > int(cart_item.product.quantity):
                return Response(
                    {'error': 'Not enough items in stock'},
                    status=status.HTTP_200_OK
                )

        total_amount = 0.0

        for cart_item in cart_items:
            total_amount += (float(cart_item.product.price)
                             * float(cart_item.count))

        # Cupones

        price_coupon = ''

        if coupon_code != '' and coupon_code != 'default':
            if Coupon.objects.filter(code__iexact=coupon_code).exists():
                price_coupon = Coupon.objects.get(
                    code=coupon_code
                )

                discount_amount = float(price_coupon.value)
                price_coupon.use()
                if discount_amount < total_amount:
                    total_amount -= discount_amount

        shipping = Shipping.objects.get(id=int(shipping_id))

        shipping_name = shipping.name
        shipping_time = shipping.time_to_delivery
        shipping_price = shipping.price

        total_amount += float(shipping_price)
        total_amount = round(total_amount, 2)

        for cart_item in cart_items:
            update_product = Product.objects.get(id=cart_item.product.id)

            # encontrar cantidad despues de coompra
            quantity = int(update_product.quantity) - int(cart_item.count)

            # obtener cantidad de producto por vender
            sold = int(update_product.sold) + int(cart_item.count)

            # actualizar el producto
            Product.objects.filter(id=cart_item.product.id).update(
                quantity=quantity, sold=sold
            )

        try:
            order = Order.objects.create(
                user=user,
                amount=total_amount,
                full_name=full_name,
                address=address,
                district=district,
                city=city,
                postal_zip_code=postal_zip_code,
                telephone_number=telephone_number,
                shipping_name=shipping_name,
                shipping_time=shipping_time,
                shipping_price=float(shipping_price)
            )
        except (RuntimeError, TypeError, NameError):
            print(NameError)
            return Response(
                {'error': 'Transaction succeeded but failed to create the order'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        print('order', order)
        for cart_item in cart_items:
            try:
                # agarrar el producto
                product = Product.objects.get(id=cart_item.product.id)

                OrderItem.objects.create(
                    product=product,
                    order=order,
                    name=product.title,
                    price=cart_item.product.price,
                    count=cart_item.count
                )
            except (RuntimeError, TypeError, NameError):
                print(NameError)

                return Response(
                    {'error': 'Transaction succeeded and order created, but failed to create an order item'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        try:
            send_mail(
                'Your Order Details',
                'Hey ' + full_name + ','
                + '\n\nWe recieved your order!'
                + '\n\nGive us some time to process your order and ship it out to you.'
                + '\n\nYou can go on your user dashboard to check the status of your order.'
                + '\n\nSincerely,'
                + '\nShop Time',
                'anthoni_pydev@anthonidev.me',
                [user.email],
                fail_silently=False
            )
        except:
            return Response(
                {'error': 'Transaction succeeded and order created, but failed to send email'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            # Vaciar carrito de compras
            CartItem.objects.filter(cart=cart).delete()

            # Actualizar carrito
            Cart.objects.filter(user=user).update(total_items=0)

        except:
            return Response(
                {'error': 'Transaction succeeded and order successful, but failed to clear cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {'success': 'Transaction successful and order was created'},
            status=status.HTTP_200_OK
        )
