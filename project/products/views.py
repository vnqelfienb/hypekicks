from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Product


class ListProductsView(ListView):
    model = Product
    template_name = "cotton/products/product_list.html"
    context_object_name = "products"


class ProductDetailsView(DetailView):
    model = Product
    template_name = "cotton/products/product_details.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch additional data to include in the template
        product = self.object
        context["images"] = product.images.all()  # All related images
        context["available_sizes"] = product.product_sizes.filter(
            availability="available"
        )  # Available sizes
        return context
