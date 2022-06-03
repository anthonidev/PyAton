from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Coupon
from .serializers import CouponSerializer

   
class CheckCouponView(APIView):
    serializer_class = CouponSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = None

    def get(self, request, format=None):
        try:
            coupon_code = request.query_params.get('coupon_code')
            if Coupon.objects.filter(code=coupon_code).exists():
                coupon = Coupon.objects.get(code=coupon_code)
                return Response(
                    {'coupon': self.serializer_class(coupon).data},
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
