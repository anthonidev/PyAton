from django.urls import path
from .views import GetOrderTotalView, ProcessOrderView

app_name="order"

urlpatterns = [
    path('get-order-total', GetOrderTotalView.as_view()),
    path('make-order', ProcessOrderView.as_view()),
]