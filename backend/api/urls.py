from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, UserViewSet

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register('users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls')),  # Пути для Djoser
    path('api/auth/', include('djoser.urls.authtoken')),  # Пути для токенов
]
