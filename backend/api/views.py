from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models import Recipe
from .serializers import RecipeIngredientWriteSerializer, RecipeIngredientReadSerializer, RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Сохраняем рецепт с автором

