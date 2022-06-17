from django.urls import path

from .views import (
    EmptyCartView,
    SynchCartView,
    CartView
)

app_name = "cart"

urlpatterns = [
    path('', CartView.as_view()),
    path('empty-cart', EmptyCartView.as_view()),
    path('synch', SynchCartView.as_view()),
]
