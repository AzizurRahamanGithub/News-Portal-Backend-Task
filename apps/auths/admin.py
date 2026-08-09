from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    def colored_role(self, obj):
        colors = {
            "user": "#6c757d", 
            "admin": "#fd7e14",  
        }
        color = colors.get(obj.role, "#6c757d")

        return format_html(
            '<span style="color:{}; font-weight:700; padding:4px 8px; border-radius:12px; background-color:{}20;">{}</span>',
            color,
            color,
            obj.get_role_display() if hasattr(obj, "get_role_display") else obj.role,
        )

    colored_role.short_description = "Role"
    colored_role.admin_order_field = "role"

    list_display = (
        "email",
        "username",
        "colored_role",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
    )

    list_filter = ("role", "is_active", "is_staff", "is_superuser", "created_at")
    search_fields = ("email", "username", "full_name", "first_name", "last_name", "phone_number")
    ordering = ("-id",)
    date_hierarchy = "created_at"

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "full_name",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "address",
                    "role",
                )
            },
        ),
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
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "role", "is_active", "is_staff"),
        }),
    )

    readonly_fields = ("created_at", "updated_at", "last_login")
