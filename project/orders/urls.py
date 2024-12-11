from django.urls import path

from .views import OrdersListView

urlpatterns = [
    path("orders-list/", OrdersListView.as_view(), name="orders_list"),
]
