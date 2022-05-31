from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Coupon
from .serializers import CouponSerializer


class CheckCouponView(APIView):
    def get(self, request, format=None):
        try:
            coupon_code = request.query_params.get('coupon_code')
            if Coupon.objects.filter(code=coupon_code).exists():
                coupon = Coupon.objects.get(code=coupon_code)
                coupon = CouponSerializer(coupon)
                return Response(
                    {'coupon': coupon.data},
                    status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {'error': 'Coupon code not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except:
            return Response(
                {'error': 'Something went wrong when checking coupon'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
