import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, DetailView, ListView, TemplateView, View
from orders.models import Order, OrderItem

from .models import CartItem, Product, ProductSize

# stripe.api_key = settings.STRIPE_SECRET_KEY

User = get_user_model()


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


class CreateStripeCheckoutSessionView(View):
    redirect_url = reverse_lazy("index")

    def post(self, request, *args, **kwargs):
        # Fetch all items in the user's cart
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect(self.redirect_url)

        line_items = []
        for item in cart_items:
            product = item.product
            line_items.append(
                {
                    "price_data": {
                        "currency": "eur",
                        "unit_amount": int(product.price * 100),
                        "product_data": {
                            "name": product.name,
                            "description": product.desc,
                            "images": [
                                f"{settings.BACKEND_DOMAIN}/{product.thumbnail.url}"
                            ],
                        },
                    },
                    "quantity": item.quantity,
                }
            )

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=settings.PAYMENT_SUCCESS_URL,
                cancel_url=settings.PAYMENT_CANCEL_URL,
                metadata={
                    "user_id": request.user.id,
                },
            )
            return redirect(checkout_session.url)

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect(self.redirect_url)


class PaymentSuccessView(TemplateView):
    template_name = "cotton/products/payment_success.html"


class PaymentCancelView(TemplateView):
    template_name = "cotton/products/payment_cancel.html"


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return JsonResponse({"error": "Invalid payload"}, status=400)
        except stripe.error.SignatureVerificationError:
            return JsonResponse({"error": "Invalid signature"}, status=400)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            self.handle_checkout_session_completed(session)

        return JsonResponse({"status": "success"}, status=200)

    def handle_checkout_session_completed(self, session):
        metadata = session.get("metadata", {})
        user_id = metadata.get("user_id")

        if not user_id:
            raise ValueError("User ID is missing in the session metadata")

        user = User.objects.get(id=user_id)
        cart_items = CartItem.objects.filter(user=user)

        order = Order.objects.create(user=user, status="ongoing")

        for item in cart_items:
            product = item.product

            if product.quantity < item.quantity:
                raise ValueError(f"Insufficient stock for {product.name}")

            product.quantity -= item.quantity
            product.save()

            order.items.create(
                product=item.product,
                size=item.size,
                quantity=item.quantity,
                price=item.product.price,
            )

            item.delete()
