from django.urls import path

from .views import (
    AddToCartView,
    DeleteCartItemView,
    ListCartView,
    ListProductsView,
    ProductDetailsView,
)

urlpatterns = [
    path("list-products/", ListProductsView.as_view(), name="products"),
    path("list-cart/", ListCartView.as_view(), name="cart_list"),
    path("add-to-cart/", AddToCartView.as_view(), name="add_to_cart"),
    path(
        "delete-cart-item/<int:pk>/",
        DeleteCartItemView.as_view(),
        name="delete_cart_item",
    ),
    path("<slug:slug>/", ProductDetailsView.as_view(), name="product_detail"),
]
