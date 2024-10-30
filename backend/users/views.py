from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.models import Recipe, Subscription
from api.pagination import CustomPagination
from api.serializers import (AvatarSerializer, PasswordChangeSerializer,
                             SubscriptionRecipeSerializer,
                             SubscriptionSerializer, UserCreateSerializer,
                             UserSerializer)
from .models import CustomUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "me", "subscriptions"]:
            return UserSerializer
        return UserCreateSerializer

    def get_serializer_context(self):

        return {"request": self.request}

    def get_subscription_data(self, user, request, recipes_limit=None):
        recipes = Recipe.objects.filter(author=user)
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]

        serialized_recipes = SubscriptionRecipeSerializer(
            recipes, many=True, context={"request": request}
        ).data

        return {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_subscribed": True,
            "avatar": (
                request.build_absolute_uri(user.avatar.url)
                if user.avatar else None
            ),
            "recipes_count": Recipe.objects.filter(author=user).count(),
            "recipes": serialized_recipes
        }

    @action(detail=True, methods=["post", "delete"], url_path="subscribe")
    def manage_subscription(self, request, pk=None):
        author = self.get_object()

        if not request.user.is_authenticated:
            raise NotAuthenticated("Необходима авторизация.")

        if request.method == "POST":
            data = {"user": request.user.id, "author": author.id}
            serializer = SubscriptionSerializer(
                data=data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            recipes_limit = request.query_params.get("recipes_limit")
            response_data = self.get_subscription_data(
                author, request, recipes_limit)
            return Response(response_data, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            subscription = Subscription.objects.filter(
                user=request.user, author=author).first()
            if not subscription:
                return Response(
                    {"detail": "Подписка не найдена."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscription.delete()
            return Response({"detail": "Вы отписались от пользователя."},
                            status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"detail": "Метод не поддерживается."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=False, methods=["get"], url_path="subscriptions")
    def subscriptions(self, request):
        user = request.user
        subscriptions = CustomUser.objects.filter(subscribers__user=user)

        paginator = self.paginator
        paginated_subscriptions = paginator.paginate_queryset(
            subscriptions, request)

        recipes_limit = request.query_params.get("recipes_limit")
        result = [
            self.get_subscription_data(author, request, recipes_limit)
            for author in paginated_subscriptions
        ]

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

        if not request.user.is_authenticated:
            return Response(
                {"detail": "Пользователь не авторизован."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if request.method == "DELETE":
            user.avatar.delete()
            user.avatar = None
            user.save()
            return Response(
                {"detail": "Avatar deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )

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
        if not user.check_password(
                serializer.validated_data["current_password"]):
            return Response(
                {"current_password": "Incorrect password"},
                status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"status": "password set"},
                        status=status.HTTP_204_NO_CONTENT)
