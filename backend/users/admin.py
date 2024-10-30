from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class BaseAdminSettings(admin.ModelAdmin):
    """Базовая кастомизация админ панели."""
    empty_value_display = "-пусто-"


class CustomUserAdmin(BaseAdminSettings, UserAdmin):
    """Кастомизация админ панели для управления пользователями."""
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("avatar", "role")}),
    )
    list_display = ("id", "role", "username",
                    "email", "first_name", "last_name")
    list_display_links = ("id", "username")
    search_fields = ("role", "username", "email")
    list_filter = ("role", "email", "username")


# Регистрируем только модель CustomUser в админке
admin.site.register(CustomUser, CustomUserAdmin)
