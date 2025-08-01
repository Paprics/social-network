from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUserModel, UserProfileModel


class UserProfileInline(admin.StackedInline):
    model = UserProfileModel
    can_delete = False
    verbose_name_plural = "User Profile"


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    model = CustomUserModel

    # Если у тебя кастомный пользователь без стандартных полей, нужно указать поля явно:
    fieldsets = (
        (None, {"fields": ("phone_number", "username", "email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "username", "email", "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "phone_number", "email", "is_staff", "is_active")
    search_fields = ("username", "phone_number", "email")
    ordering = ("username",)


admin.site.register(CustomUserModel, CustomUserAdmin)
admin.site.register(UserProfileModel)
