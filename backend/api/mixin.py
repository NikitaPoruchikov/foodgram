from rest_framework.response import Response
from rest_framework import status


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
            serializer = serializer_class(recipe, context={'request': request})
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
