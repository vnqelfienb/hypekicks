from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


def get_image_filename(instance, filename):
    # Ensure the instance is of type Product and has the required attribute
    if hasattr(instance, "name"):
        slug = slugify(instance.name)
        return f"sneakers/{slug}-{filename}"
    else:
        # Fallback in case the instance is not a Product object
        return f"sneakers/default-{filename}"


class ProductTag(models.Model):
    name = models.CharField(
        max_length=100, unique=True, help_text=_("Designates the name of the tag.")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Size(models.Model):
    size = models.CharField(max_length=10, unique=True)
    availability = models.CharField(
        max_length=20,
        choices=[("available", "Available"), ("out_of_stock", "Out of Stock")],
        default="available",
    )

    def __str__(self):
        return f"Size {self.size} ({self.availability})"


class ProductSize(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="product_sizes"
    )
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    availability = models.CharField(
        max_length=20,
        choices=[("available", "Available"), ("out_of_stock", "Out of Stock")],
        default="available",
    )

    def __str__(self):
        return f"{self.product.name} - Size {self.size.size} ({self.availability})"


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True, editable=True)
    brand = models.CharField(max_length=100, help_text=_("Brand of the sneaker"))
    tags = models.ManyToManyField(ProductTag, blank=True)
    desc = models.TextField(_("Description"), blank=True)
    thumbnail = models.ImageField(
        upload_to=get_image_filename,
        blank=True,
        default="sneakers/default-thumbnail.jpg",
    )
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(
        default=1, validators=[MinValueValidator(0)], help_text=_("Available stock")
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("available", _("Available")),
            ("out_of_stock", _("Out of Stock")),
            ("discontinued", _("Discontinued")),
        ],
        default="available",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        sizes = ", ".join(
            [
                str(size.size)
                for size in self.product_sizes.all()
                if size.availability == "available"
            ]
        )
        return f"{self.brand} {self.name} (Available Sizes: {sizes})"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=get_image_filename)
    is_main = models.BooleanField(default=False, help_text=_("Is this the main image?"))

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"
