from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = (
        "user",
        "username",
        "first_name",
        "last_name",
        "phone_number",
        "address",
        "created_at",
        "updated_at",
    )
    search_fields = ("user__email", "username", "first_name", "last_name")
    list_filter = ("created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "username",
                    "first_name",
                    "last_name",
                    "address",
                    "phone_number",
                )
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
    ordering = ("user",)


admin.site.register(Profile, ProfileAdmin)
