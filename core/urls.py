from django.urls import path, include
from django.contrib import admin

urlpatterns = [

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
    path('api/product/', include('apps.product.urls')),
    # path('api/account/', include('apps.account.urls')),
    path('api/cart/', include('apps.cart.urls')),
    # path('api/wishlist/', include('apps.wishlist.urls')),
    # path('api/shipping/', include('apps.shipping.urls')),
    # path('api/coupon/', include('apps.coupon.urls')),
    # path('api/order/', include('apps.order.urls')),
    # path('api/payment/', include('apps.payment.urls')),

    path('', admin.site.urls),
]