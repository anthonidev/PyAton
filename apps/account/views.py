from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer



class GetUserProfileView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)

            return Response(
                {'profile': user_profile.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving profile'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# class UpdateUserProfileView(APIView):
#     def put(self, request, format=None):
#         try:
#             user = self.request.user
#             data = self.request.data

#             address_line_1 = data['address_line_1_form']
#             address_line_2 = data['address_line_2_form']
#             city = data['city_form']
#             phone = data['phone_form']
#             zipcode = data['zipcode_form']
#             enterprise=data['enterprise_form']
#             district=data['district_form']

#             UserProfile.objects.filter(user=user).update(
#                 address_line_1=address_line_1,
#                 address_line_2=address_line_2,
#                 city=city,
#                 zipcode=zipcode,
#                 phone=phone,
#                 enterprise=enterprise,
#                 district=district
#             )

#             user_profile = UserProfile.objects.get(user=user)
#             user_profile = UserProfileSerializer(user_profile)

#             return Response(
#                 {'profile': user_profile.data},
#                 status=status.HTTP_200_OK
#             )
#         except:
#             return Response(
#                 {'error': 'Something went wrong when updating profile'},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )