from api.models import Subscription
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class BaseAdminSettings(admin.ModelAdmin):
    """Базовая кастомизация админ панели."""
    empty_value_display = '-пусто-'


class CustomUserAdmin(BaseAdminSettings, UserAdmin):
    """Кастомизация админ панели для управления пользователями."""
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('avatar', 'role')}),
    )
    list_display = ('id', 'role', 'username',
                    'email', 'first_name', 'last_name')
    list_display_links = ('id', 'username')
    search_fields = ('role', 'username', 'email')
    list_filter = ('role', 'email', 'username')


class SubscriptionAdmin(BaseAdminSettings):
    """Кастомизация админ панели для управления подписками."""
    list_display = ('id', 'user', 'author')
    list_display_links = ('id', 'user')
    search_fields = ('user__username', 'author__username')
    list_filter = ('user', 'author')


# Регистрируем модели в админке
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
