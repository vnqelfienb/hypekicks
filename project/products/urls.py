from django.urls import path

from .views import (
    AddToCartView,
    CreateStripeCheckoutSessionView,
    DeleteCartItemView,
    ListCartView,
    ListProductsView,
    PaymentCancelView,
    PaymentSuccessView,
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
    path(
        "create-checkout-session/",
        CreateStripeCheckoutSessionView.as_view(),
        name="create_checkout_session",
    ),
    path("payment-success/", PaymentSuccessView.as_view(), name="payment_success"),
    path("payment-cancel/", PaymentCancelView.as_view(), name="payment_cancel"),
    path("<slug:slug>/", ProductDetailsView.as_view(), name="product_detail"),
]
