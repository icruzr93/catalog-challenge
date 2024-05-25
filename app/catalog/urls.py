from django.urls import path

from .views import (
    BrandDetailView,
    BrandListCreateView,
    ProductDetailView,
    ProductListCreateView,
)

urlpatterns = [
    path("brands/", BrandListCreateView.as_view(), name="brands"),
    path("brands/<int:pk>/", BrandDetailView.as_view(), name="brand-detail"),
    path("products/", ProductListCreateView.as_view(), name="products"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
]
