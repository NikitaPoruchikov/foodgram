from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models import (
    Recipe,
    Tag,
    Ingredient,
    RecipeIngredient,
    ShoppingCart,
    Subscription,
    Favorite,
)
from .serializers import (
    RecipeIngredientWriteSerializer,
    RecipeIngredientReadSerializer,
    RecipeSerializer,
    UserSerializer,
    AvatarSerializer,
    TagSerializer,
    IngredientSerializer,
    SubscriptionRecipeSerializer,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserCreateSerializer, PasswordChangeSerializer
from django.contrib.auth import get_user_model
from users.models import CustomUser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RecipeFilter
from rest_framework.pagination import PageNumberPagination
from .permissions import (
    IsAuthenticatedForFilter,
    IsAuthenticatedOrCreate,
    IsOwnerOrReadOnly,
)
from rest_framework.exceptions import NotAuthenticated
from rest_framework import serializers

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by("id")
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_permissions(self):
        # Для действий, которые не требуют авторизации, оставляем доступ для всех
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticatedForFilter()]

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        # Проверяем, аутентифицирован ли пользователь

        if not self.request.user.is_authenticated:
            raise NotAuthenticated("Необходима авторизация для создания рецепта.")

        # Сохраняем рецепт с автором
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        recipe = self.get_object()

        # Проверка на авторизацию и авторство
        if request.user.is_anonymous:
            return Response(
                {"detail": "Необходима авторизация."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if recipe.author != request.user:
            return Response(
                {"detail": "Удаление чужих рецептов запрещено."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Если это ваш рецепт, выполняем удаление
        self.perform_destroy(recipe)
        return Response(
            {"detail": "Рецепт успешно удалён."}, status=status.HTTP_204_NO_CONTENT
        )

    def update(self, request, *args, **kwargs):
        recipe = self.get_object()  # Получаем объект рецепта
        # Проверяем, является ли пользователь автором

        if request.user.is_anonymous:
            return Response(
                {"detail": "Необходима авторизация."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if recipe.author != request.user:
            return Response(
                {"detail": "У вас нет прав на изменение этого рецепта."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Проверка, передано ли поле 'ingredients'
        if "ingredients" not in request.data:
            return Response(
                {"ingredients": "Это поле обязательно."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Проверка, передано ли поле 'tags'
        if "tags" not in request.data:
            return Response(
                {"tags": "Это поле обязательно."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Если все проверки пройдены, выполняем обновление
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        recipe = self.get_object()
        
        # Проверяем, авторизован ли пользователь
        if request.user.is_anonymous:
            return Response(
                {"detail": "Необходима авторизация."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Проверяем, является ли пользователь автором рецепта
        if recipe.author != request.user:
            return Response(
                {"detail": "У вас нет прав на изменение этого рецепта."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Выполняем частичное обновление, если проверки пройдены
        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=["get"], url_path="get-link")
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        short_link = f"https://foodgram.example.org/s/{recipe.id}"
        return Response({"short-link": short_link}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post", "delete"], url_path="favorite")
    def manage_favorite(self, request, pk=None):
        user = request.user
        recipe = self.get_object()

        if not request.user.is_authenticated:
            return Response(
                {"detail": "Необходима авторизация."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Если это POST-запрос, добавляем рецепт в избранное
        if request.method == "POST":
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"detail": "Рецепт уже в избранном."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Favorite.objects.create(user=user, recipe=recipe)

            # Возвращаем корректные данные о рецепте
            response_data = {
                "id": recipe.id,
                "name": recipe.name,
                "image": request.build_absolute_uri(recipe.image.url),
                "cooking_time": recipe.cooking_time,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        # Если это DELETE-запрос, удаляем рецепт из избранного
        elif request.method == "DELETE":
            favorite_item = Favorite.objects.filter(user=user, recipe=recipe)
            if not favorite_item.exists():
                return Response(
                    {"detail": "Рецепт не найден в избранном."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            favorite_item.delete()
            return Response(
                {"detail": "Рецепт удален из избранного."},
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(detail=False, methods=["get"], url_path="download_shopping_cart")
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(user=user)
        if not shopping_cart.exists():
            return Response(
                {"detail": "Корзина пуста."}, status=status.HTTP_400_BAD_REQUEST
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
        response["Content-Disposition"] = 'attachment; filename="shopping_list.txt"'
        return response

    @action(detail=True, methods=["post", "delete"], url_path="shopping_cart")
    def add_and_remove_shopping_cart(self, request, pk=None):
        user = request.user
        recipe = self.get_object()

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Необходима авторизация."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Если это POST-запрос, добавляем рецепт в корзину
        if request.method == "POST":
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"detail": "Рецепт уже добавлен в корзину."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            ShoppingCart.objects.create(user=user, recipe=recipe)

            # Формируем правильный ответ с данными о рецепте
            response_data = {
                "id": recipe.id,
                "name": recipe.name,
                "image": request.build_absolute_uri(recipe.image.url),
                "cooking_time": recipe.cooking_time,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        # Если это DELETE-запрос, удаляем рецепт из корзины
        elif request.method == "DELETE":
            cart_item = ShoppingCart.objects.filter(user=user, recipe=recipe)
            if not cart_item.exists():
                return Response(
                    {"detail": "Рецепта нет в корзине."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            cart_item.delete()
            return Response(
                {"detail": "Рецепт удален из корзины покупок."},
                status=status.HTTP_204_NO_CONTENT,
            )

    def get_serializer_class(self):
        return RecipeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        # Для действий 'list' и 'retrieve' используем UserSerializer
        if self.action in ["list", "retrieve", "me", "subscriptions"]:
            return UserSerializer
        # Для всех остальных действий (например, создание пользователя) используем UserCreateSerializer
        return UserCreateSerializer

    def get_serializer_context(self):

        return {"request": self.request}

    @action(detail=True, methods=["post", "delete"], url_path="subscribe")
    def manage_subscription(self, request, pk=None):
        user = request.user
        author = self.get_object()

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            raise NotAuthenticated(
                "Необходима авторизация для выполнения данного действия."
            )

        if request.method == "POST":
            # Проверяем, есть ли подписка
            if Subscription.objects.filter(user=user, author=author).exists():
                return Response(
                    {"detail": "Вы уже подписаны на этого пользователя."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Запрещаем подписываться на самого себя
            if user == author:
                return Response(
                    {"detail": "Нельзя подписаться на самого себя."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Создаем подписку
            Subscription.objects.create(user=user, author=author)

            # Лимит на количество рецептов
            recipes_limit = request.query_params.get("recipes_limit")
            recipes = Recipe.objects.filter(author=author)
            if recipes_limit:
                recipes = recipes[: int(recipes_limit)]

            serialized_recipes = SubscriptionRecipeSerializer(
                recipes, many=True, context={"request": request}
            ).data
            response_data = {
                "id": author.id,
                "username": author.username,
                "first_name": author.first_name,
                "last_name": author.last_name,
                "email": author.email,
                "is_subscribed": True,
                "avatar": (
                    request.build_absolute_uri(author.avatar.url)
                    if author.avatar
                    else None
                ),
                "recipes_count": Recipe.objects.filter(author=author).count(),
                "recipes": serialized_recipes,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            # Проверяем, есть ли подписка на этого пользователя
            subscription = Subscription.objects.filter(user=user, author=author).first()
            if not subscription:
                # Если подписка не существует, возвращаем 400
                return Response(
                    {"detail": "Подписка не найдена."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Если подписка существует, удаляем её
            subscription.delete()
            return Response(
                {"detail": "Вы отписались от пользователя."},
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(detail=False, methods=["get"], url_path="subscriptions")
    def subscriptions(self, request):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)

        paginator = CustomPagination()
        paginated_subscriptions = paginator.paginate_queryset(subscriptions, request)

        if paginated_subscriptions is None:
            return Response(
                {"detail": "Нет подписок."}, status=status.HTTP_204_NO_CONTENT
            )

        # Получаем параметр recipes_limit из запроса, если он есть
        recipes_limit = request.query_params.get("recipes_limit")
        if recipes_limit:
            try:
                recipes_limit = int(recipes_limit)
            except ValueError:
                return Response(
                    {"detail": "Параметр recipes_limit должен быть числом."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            recipes_limit = 3  # значение по умолчанию, если параметр не передан

        result = []
        for subscription in paginated_subscriptions:
            author = subscription.author
            # Используем recipes_limit для ограничения количества рецептов
            recipes = Recipe.objects.filter(author=author)[:recipes_limit]
            result.append(
                {
                    "id": author.id,
                    "email": author.email,
                    "username": author.username,
                    "first_name": author.first_name,
                    "last_name": author.last_name,
                    "is_subscribed": True,
                    "recipes": SubscriptionRecipeSerializer(
                        recipes, many=True, context={"request": request}
                    ).data,
                    "recipes_count": recipes.count(),
                    "avatar": (
                        request.build_absolute_uri(author.avatar.url)
                        if author.avatar
                        else None
                    ),
                }
            )

        return paginator.get_paginated_response(result)

    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["put", "delete"], url_path="me/avatar")
    def update_avatar(self, request):
        user = request.user

        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Пользователь не авторизован."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if request.method == "DELETE":
            # Обрабатываем удаление аватара
            user.avatar.delete()  # Удаляем файл аватара
            user.avatar = None  # Обнуляем поле avatar в базе
            user.save()
            return Response(
                {"detail": "Avatar deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )

        # Обрабатываем обновление аватара (PUT)
        serializer = AvatarSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="set_password")
    def set_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data["current_password"]):
            return Response({"current_password": "Incorrect password"}, status=400)
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"status": "password set"}, status=204)


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
