from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, View

from .models import CartItem, Product, ProductSize


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
        product = self.object
        context["images"] = product.images.all()  # All related images
        context["available_sizes"] = product.product_sizes.filter(
            availability="available"
        )
        return context


class AddToCartView(LoginRequiredMixin, View):
    redirect_url = reverse_lazy("index")

    def post(self, request, *args, **kwargs):
        # Extract product and size IDs from the request
        product_id = request.POST.get("product_id")
        size_id = request.POST.get("size_id")

        product = get_object_or_404(Product, id=product_id)
        size = get_object_or_404(ProductSize, id=size_id)

        if size.availability != "available":
            messages.error(request, "The selected size is out of stock.")
            return redirect(self.redirect_url)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product, size=size
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, "Item added to cart.")
        return redirect(self.redirect_url)


class ListCartView(ListView):
    model = CartItem
    template_name = "cotton/cart/cart_list.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        total_price = sum(
            item.product.price * item.quantity for item in self.object_list
        )

        if request.htmx:
            return render(
                request,
                self.template_name,
                {
                    "cart_items": self.object_list,
                    "total_price": total_price,
                },
            )


class DeleteCartItemView(DeleteView):
    model = CartItem
    template_partial = "cotton/cart/cart_list.html"

    def delete(self, request, *args, **kwargs):
        if request.htmx:
            item_id = kwargs.get("pk")
            cart_item = CartItem.objects.filter(id=item_id, user=request.user).first()

            if not cart_item:
                return JsonResponse(
                    {"error": "Item not found or already deleted."}, status=404
                )

            cart_item.delete()

            cart_items = CartItem.objects.filter(user=request.user)
            total_price = sum(item.product.price * item.quantity for item in cart_items)

            return render(
                request,
                self.template_partial,
                {"cart_items": cart_items, "total_price": total_price},
            )
