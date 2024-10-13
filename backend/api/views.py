from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models import Recipe
from .serializers import RecipeIngredientWriteSerializer, RecipeIngredientReadSerializer, RecipeSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer, PasswordChangeSerializer
from django.contrib.auth import get_user_model
from users.models import CustomUser

User = get_user_model()

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Сохраняем рецепт с автором

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='set_password')
    def set_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['current_password']):
            return Response({"current_password": "Incorrect password"}, status=400)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"status": "password set"}, status=204)
