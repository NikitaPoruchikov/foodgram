from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import RecipeFilter
from .mixin import AddRemoveMixin, AuthorPermissionMixin
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          SubscriptionRecipeSerializer, TagSerializer)

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet,
                    AddRemoveMixin, AuthorPermissionMixin):
    queryset = Recipe.objects.all().order_by("id")
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["get"], url_path="get-link")
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        short_link = f"https://foodgram.example.org/s/{recipe.id}"
        return Response({"short-link": short_link}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post", "delete"], url_path="favorite",
            permission_classes=[permissions.IsAuthenticated])
    def manage_favorite(self, request, pk=None):
        return self.add_or_remove(
            request, Favorite, SubscriptionRecipeSerializer)

    @action(detail=False, methods=["get"], url_path="download_shopping_cart",
            permission_classes=[permissions.IsAuthenticated])
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

    @action(detail=True, methods=["post", "delete"], url_path="shopping_cart",
            permission_classes=[permissions.IsAuthenticated])
    def add_and_remove_shopping_cart(self, request, pk=None):
        return self.add_or_remove(
            request, ShoppingCart, SubscriptionRecipeSerializer)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get("name", None)
        if name:
            return queryset.filter(name__icontains=name)
        return queryset
