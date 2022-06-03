
# Create your views here.
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Shipping
from .serializers import ShippingSerializer
from rest_framework import generics


class GetShippingView(generics.ListAPIView):
    serializer_class = ShippingSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Shipping.objects.order_by('price').all()

    def list(self, request, format=None):
        if Shipping.objects.all().exists():
            queryset = self.get_queryset()
            return Response(
                {'shipping': self.serializer_class(
                    queryset, many=True).data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'No shipping options available'},
                status=status.HTTP_404_NOT_FOUND
            )
