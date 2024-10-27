from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import RecipeFilter
from .mixin import AddRemoveMixin, AuthorPermissionMixin
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)
from .pagination import CustomPagination
from .permissions import IsAuthenticatedForFilter, IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          SubscriptionRecipeSerializer, TagSerializer)

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet,
                    AddRemoveMixin, AuthorPermissionMixin):
    queryset = Recipe.objects.all().order_by("id")
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticatedForFilter()]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated(
                "Необходима авторизация для создания рецепта.")
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_author_permission(request, obj)  # Проверка
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_author_permission(request, obj)  # Проверка
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get"], url_path="get-link")
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        short_link = f"https://foodgram.example.org/s/{recipe.id}"
        return Response({"short-link": short_link}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post", "delete"], url_path="favorite")
    def manage_favorite(self, request, pk=None):
        return self.add_or_remove(
            request, Favorite, SubscriptionRecipeSerializer)

    @action(detail=False, methods=["get"], url_path="download_shopping_cart")
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(user=user)
        if not shopping_cart.exists():
            return Response(
                {"detail": "Корзина пуста."},
                status=status.HTTP_400_BAD_REQUEST
            )

        shopping_list = {}
        for item in shopping_cart:
            ingredients = RecipeIngredient.objects.filter(recipe=item.recipe)
            for ingredient in ingredients:
                name = ingredient.ingredient.name
                amount = ingredient.amount
                unit = ingredient.ingredient.measurement_unit
                if name in shopping_list:
                    shopping_list[name]["amount"] += amount
                else:
                    shopping_list[name] = {"amount": amount, "unit": unit}

        # Формируем список покупок (пример с текстом)
        shopping_text = "Список покупок:\n\n"
        for name, data in shopping_list.items():
            shopping_text += f"{name} - {data['amount']} {data['unit']}\n"

        response = HttpResponse(shopping_text, content_type="text/plain")
        response["Content-Disposition"] = (
            'attachment; filename="shopping_list.txt"')
        return response

    @action(detail=True, methods=["post", "delete"], url_path="shopping_cart")
    def add_and_remove_shopping_cart(self, request, pk=None):
        return self.add_or_remove(
            request, ShoppingCart, SubscriptionRecipeSerializer)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]

    def get_queryset(self):
        name = self.request.query_params.get("name", None)
        if name:
            return self.queryset.filter(name__istartswith=name)
        return self.queryset
