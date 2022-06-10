from django.urls import path
from .views import WishListView

app_name = "wishlist"

urlpatterns = [
    path('wishlist', WishListView.as_view()),
]
