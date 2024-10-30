from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.response import Response


class AddRemoveMixin:
    def add_or_remove(self, request, model, serializer_class):
        user = request.user
        recipe = self.get_object()

        if not user.is_authenticated:
            return Response(
                {"detail": "Необходима авторизация."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if request.method == "POST":
            if model.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"detail": "Рецепт уже добавлен."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            model.objects.create(user=user, recipe=recipe)
            serializer = serializer_class(recipe, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            instance = model.objects.filter(user=user, recipe=recipe)
            if not instance.exists():
                return Response(
                    {"detail": "Рецепт не найден."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "Метод не поддерживается."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class AuthorPermissionMixin:
    def check_author_permission(self, request, obj):
        # Проверка аутентификации
        if not request.user.is_authenticated:
            raise NotAuthenticated(detail="Необходима авторизация.")
        # Проверка прав (авторства)
        if obj.author != request.user:
            raise PermissionDenied(
                detail="У вас нет прав на выполнение этого действия.")
