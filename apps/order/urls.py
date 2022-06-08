from django.urls import path
from .views import GetOrderTotalView, ProcessOrderView,OrderView

app_name="order"

urlpatterns = [
    path('get-order-total', GetOrderTotalView.as_view()),
    path('make-order', ProcessOrderView.as_view()),
    path('get-my-orden', OrderView.as_view()),
]