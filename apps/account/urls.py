from django.urls import path

from .views import AddressView, GetUserProfileView, UpdateUserProfileView
app_name = "account"

urlpatterns = [
    path('user', GetUserProfileView.as_view()),
    path('update', UpdateUserProfileView.as_view()),
    path('address', AddressView.as_view()),
]

