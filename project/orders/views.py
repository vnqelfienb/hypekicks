from django.http import JsonResponse
from django.views.generic.list import ListView

from .models import Order


class OrdersListView(ListView):
    model = Order
    template_name = "cotton/orders/orders_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        # Filter orders by user and status
        status = self.request.GET.get("status", "ongoing")
        return Order.objects.filter(user=self.request.user, status=status)
