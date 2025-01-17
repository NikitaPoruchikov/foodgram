from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     Subscription, Tag)


class BaseAdminSettings(admin.ModelAdmin):
    """Общие настройки для админ-панели."""
    empty_value_display = "пусто"


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1  # Количество пустых полей для добавления новых ингредиентов
    autocomplete_fields = ['ingredient']


@admin.register(Tag)
class TagAdmin(BaseAdminSettings):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Ingredient)
class IngredientAdmin(BaseAdminSettings):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(BaseAdminSettings):
    list_display = ("recipe", "ingredient", "amount")
    list_filter = ("ingredient",)
    search_fields = ["^name"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "cooking_time", "get_favorite_count")
    search_fields = ("name", "author__username")
    list_filter = ("tags", "author")
    filter_horizontal = ("tags",)
    readonly_fields = ("get_favorite_count",)
    inlines = [RecipeIngredientInline]

    def get_favorite_count(self, obj):
        return obj.favorited_by.count()
    get_favorite_count.short_description = "Количество добавлений в избранное"


@admin.register(Subscription)
class SubscriptionAdmin(BaseAdminSettings):
    list_display = ("user", "author", "created_at")
    search_fields = ("user__username", "author__username")
    list_filter = ("author", "user")


@admin.register(Favorite)
class FavoriteAdmin(BaseAdminSettings):
    list_display = ("user", "recipe", "added_at")
    search_fields = ("user__username", "recipe__name")
    list_filter = ("user",)
