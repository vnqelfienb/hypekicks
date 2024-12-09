from django.contrib import admin

from .models import Product, ProductImage, ProductSize, ProductTag, Size


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "brand", "price", "status", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "brand")
    list_filter = ("status", "brand")
    ordering = ("-created_at",)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "is_main", "created_at")
    list_filter = ("product", "is_main")
    search_fields = ("product__name",)


class SizeAdmin(admin.ModelAdmin):
    list_display = ("size", "availability")
    list_filter = ("availability",)
    search_fields = ("size",)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductTag)
admin.site.register(Size, SizeAdmin)
admin.site.register(ProductSize)
