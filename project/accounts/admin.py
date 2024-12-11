from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin, ModelAdmin):
    model = CustomUser
    list_display = (
        "email",
        "is_active",
        "is_staff",
        "verification_status",
        "groups_list",
    )
    search_fields = ("email",)
    list_filter = ("is_active", "is_staff", "verification_status")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("verification_status",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ((None, {"fields": ("email", "password1", "password2")}),)
    ordering = ("email",)

    def groups_list(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])

    groups_list.short_description = _("Groups")


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    model = Group
    list_display = ("name", "permissions_count")
    search_fields = ("name",)
    ordering = ("name",)

    def permissions_count(self, obj):
        return obj.permissions.count()

    permissions_count.short_description = _("Permissions Count")


admin.site.register(CustomUser, CustomUserAdmin)
