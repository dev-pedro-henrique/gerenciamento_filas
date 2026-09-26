from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import LoginAttempt, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ("name", "username")
    list_display = ("username", "name", "role", "is_active", "date_joined")
    list_filter = ("role", "is_active")
    search_fields = ("username", "name")
    readonly_fields = ("date_joined", "last_login", "active_session_key")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Identificação", {"fields": ("name", "role")}),
        ("Estado", {"fields": ("is_active", "last_login", "date_joined")}),
        (
            "Permissões administrativas",
            {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Sessão", {"fields": ("active_session_key",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "name", "role", "password1", "password2"),
            },
        ),
    )


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ("username", "failed_attempts", "locked_until", "updated_at")
    search_fields = ("username",)
    readonly_fields = ("username", "failed_attempts", "locked_until", "updated_at")
