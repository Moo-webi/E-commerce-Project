from django.urls import path
from .views import LatestProductList, search
from .views import ProductDetail, CategoryDetail

urlpatterns = [
    path('latest-products/', LatestProductList.as_view(), name='latest-products'),
    path('products/<slug:category_slug>/<slug:product_slug>/', ProductDetail.as_view(), ),
    path('products/<slug:category_slug>/', CategoryDetail.as_view() ),
    path('products/search', search),

]