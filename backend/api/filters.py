import django_filters
from django_filters import rest_framework as filters

from .models import Recipe, Tag


class RecipeFilter(filters.FilterSet):
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_is_in_shopping_cart")
    is_favorited = filters.BooleanFilter(
        method="filter_is_favorited")
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=Tag.objects.all(), to_field_name="slug"
    )

    class Meta:
        model = Recipe
        fields = ["tags", "author", "is_favorited", "is_in_shopping_cart"]

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = getattr(self.request, "user", None)
        if value and user.is_authenticated:
            return queryset.filter(in_cart__user=user)
        elif value is False and user.is_authenticated:
            return queryset.exclude(in_cart__user=user)
        return queryset

    # Фильтрация по параметру `is_favorited`
    def filter_is_favorited(self, queryset, name, value):
        user = getattr(self.request, "user", None)
        if value and user.is_authenticated:
            return queryset.filter(favorited_by__user=user)
        elif value is False and user.is_authenticated:
            return queryset.exclude(favorited_by__user=user)
        return queryset
