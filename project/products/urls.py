from django.urls import path

from .views import ListProductsView, ProductDetailsView

urlpatterns = [
    path("list-products/", ListProductsView.as_view(), name="products"),
    path("<slug:slug>/", ProductDetailsView.as_view(), name="product_detail"),
]
