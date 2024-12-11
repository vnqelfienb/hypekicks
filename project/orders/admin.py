from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Removes extra blank rows
    readonly_fields = ("product", "size", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "id")
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]

    actions = ["mark_as_completed", "mark_as_cancelled", "delete_orders"]

    def get_readonly_fields(self, request, obj=None):
        # Make fields readonly after creation
        if obj:
            return ["user", "status", "created_at"]
        return []

    def mark_as_completed(self, request, queryset):
        queryset.update(status="completed")
        self.message_user(request, "Selected orders have been marked as completed.")

    mark_as_completed.short_description = "Mark selected orders as completed"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status="cancelled")
        self.message_user(request, "Selected orders have been marked as cancelled.")

    mark_as_cancelled.short_description = "Mark selected orders as cancelled"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "size", "quantity", "price")
    list_filter = ("product",)
    search_fields = ("product__name", "order__id")
