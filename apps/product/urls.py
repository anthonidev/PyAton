from django.urls import path

from apps.product.views import (
    BrandsCategoryView,
    GetSubCategoryView,
    ListBrandView,
    ListBySearchView,
    ListCategoryView,
    ListProductView,
    ListProductsHomeView,
    ProductDetailView,
    ProductsCategoryView,
    ProductDetailView
)

app_name = "product"

urlpatterns = [
    path('categories', ListCategoryView.as_view()),
    path('products_homepage', ListProductsHomeView.as_view()),
    path('brands', ListBrandView.as_view()),
    path('products', ListProductView.as_view()),
    path('filter', ListBySearchView.as_view()),
    # path('<slug>', ProductDetailView.as_view()),
    path('category/<slug>', ProductsCategoryView.as_view()),
    path('category/subcategory/<slug>', GetSubCategoryView.as_view()),
    path('brand/<id>', BrandsCategoryView.as_view()),
    
    path('<slug>', ProductDetailView.as_view()),
]
