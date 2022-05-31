from math import e
from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.cart.models import Cart, CartItem
from apps.coupon.models import Coupon
from apps.order.models import Order, OrderItem
from apps.product.models import Product
from apps.shipping.models import Shipping
from django.core.mail import send_mail

# Create your views here.


class GetOrderTotalView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        # tax = 0.18

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

                # Impuesto
                # estimated_tax = round(total_amount * tax, 2)

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
                    # 'estimated_tax': f'{estimated_tax:.2f}',
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

        full_name = data['full_name']
        address_line_1 = data['address_line_1']
        address_line_2 = data['address_line_2']
        city = data['city']
        district = data['district']
        postal_zip_code = data['zipcode']
        telephone_number = data['telephone_number']

        # revisar si datos de shipping son validos
        

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

        # revisar si hay stock

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
                price_coupon.use
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

            # crear orden
        
        # print("user",user)
        # print("code",f'{full_name} {total_amount} {postal_zip_code}')
        # print("amout",total_amount)
        # print("fullname",full_name)
        # print("address_line_1",address_line_1)
        # print("address_line_2",address_line_2)
        # print("city",city)
        # print("postal_zip_code",postal_zip_code)
        # print("telephone_number",telephone_number)
        # print("shipping_name",shipping_name)
        # print("shipping_time",shipping_time)
        # print("shipping_price",float(shipping_price))
        # print("district",district)
       
        try:
            order = Order.objects.create(
                user=user,
                transaction_id=f'{full_name} {total_amount} {postal_zip_code}',
                amount=total_amount,
                full_name=full_name,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
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
        print('order',order)
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

        # try:
        #     send_mail(
        #         'Your Order Details',
        #         'Hey ' + full_name + ','
        #         + '\n\nWe recieved your order!'
        #         + '\n\nGive us some time to process your order and ship it out to you.'
        #         + '\n\nYou can go on your user dashboard to check the status of your order.'
        #         + '\n\nSincerely,'
        #         + '\nShop Time',
        #         'mail@mail.com',
        #         [user.email],
        #         fail_silently=False
        #     )
        # except:
        #     return Response(
        #         {'error': 'Transaction succeeded and order created, but failed to send email'},
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )

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
      