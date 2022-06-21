from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions

from apps.user.models import UserAccount
from .models import UserAddress, UserProfile
from .serializers import UserAddressSerializer, UserProfileSerializer
import cloudinary


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


class UpdateUserProfileView(APIView):
    def put(self, request):
        try:
            user = self.request.user
            data = self.request.data
            dni = data['dni']
            dob = data['dob']
            image = data['image']
            first_name = data['first_name']
            last_name = data['last_name']
            treatment = data['treatment']

            try:
                img = cloudinary.uploader.upload(image)

                UserProfile.objects.filter(user=user).update(
                    treatment=treatment,
                    dni=dni,
                    dob=dob,
                    photo=img['secure_url'],
                )
            except Exception as e:
                print(e)
                return Response(
                    {'error': 'Something went wrong when updating profile'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)

            UserAccount.objects.filter(id=user.id).update(
                first_name=first_name,
                last_name=last_name,
            )

            return Response(
                {'profile': user_profile.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when updating profile'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AddressView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = None
    serializer_class = UserAddressSerializer

    def get(self, request, format=None):
        try:
            user = self.request.user
            user_profile = UserProfile.objects.get(user=user)

            address_user = UserAddress.objects.filter(account=user_profile)

            address_user = UserAddressSerializer(
                address_user, many=True, context={'request': request})

            return Response(
                {'address': address_user.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving profile'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            data = self.request.data
            user = self.request.user

            first_name = data['first_name']
            last_name = data['last_name']
            enterprise = data['enterprise']
            address = data['address']
            zipcode = data['zipcode']
            district = data['district']
            city = data['city']
            phone = data['phone']

            if not enterprise:
                enterprise = ''

            if not zipcode:
                zipcode = ''
            user_profile = UserProfile.objects.get(user=user)

            UserAddress.objects.create(
                account=user_profile,
                first_name=first_name,
                last_name=last_name,
                enterprise=enterprise,
                address=address,
                zipcode=zipcode,
                district=district,
                city=city,
                phone=phone
            )

            result = UserAddress.objects.filter(account=user_profile)

            result = UserAddressSerializer(
                result, many=True, context={'request': request})

            return Response(
                {'address': result.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving profile'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, format=None):
        try:
            data = self.request.data
            user = self.request.user
            address_id = data['id']
            first_name = data['first_name']
            last_name = data['last_name']
            enterprise = data['enterprise']
            address = data['address']
            zipcode = data['zipcode']
            district = data['district']
            city = data['city']
            phone = data['phone']
            if not enterprise:
                enterprise = ''
            if not zipcode:
                zipcode = ''
            user_profile = UserProfile.objects.get(user=user)
            UserAddress.objects.filter(account=user_profile, id=address_id).update(
                first_name=first_name,
                last_name=last_name,
                enterprise=enterprise,
                address=address,
                zipcode=zipcode,
                district=district,
                city=city,
                phone=phone
            )
            result = UserAddress.objects.filter(account=user_profile)

            result = UserAddressSerializer(
                result, many=True, context={'request': request})

            return Response(
                {'address': result.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving profile'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, format=None):
        try:
            address_id = request.query_params.get('id')
            user = self.request.user

            user_profile = UserProfile.objects.get(user=user)
            UserAddress.objects.filter(
                account=user_profile, id=address_id).delete()
            result = UserAddress.objects.filter(account=user_profile)

            result = UserAddressSerializer(
                result, many=True, context={'request': request})
            return Response(
                {'address': result.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving profile'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
