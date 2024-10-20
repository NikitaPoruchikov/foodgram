from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsAuthenticatedForFilter(permissions.BasePermission):
    """
    Разрешает доступ к рецептам только для авторизованных пользователей,
    если они используют параметры фильтрации `is_favorited` или `is_in_shopping_cart`.
    """

    def has_permission(self, request, view):
        # Параметры, которые требуют авторизации
        filter_params = ['is_favorited', 'is_in_shopping_cart']

        # Если запрос не содержит фильтров или пользователь пытается просто получить список рецептов
        if not any(param in request.query_params for param in filter_params):
            return True

        # Если пользователь пытается фильтровать по `is_favorited` или `is_in_shopping_cart`
        # проверяем, что он авторизован
        return request.user and request.user.is_authenticated


class IsAuthenticatedOrCreate(BasePermission):
    """
    Разрешает доступ для всех при регистрации (действие create),
    а для остальных действий требует аутентификацию.
    """

    def has_permission(self, request, view):
        # Если пользователь пытается зарегистрироваться (POST запрос на создание)
        if view.action == 'create':
            return True
        # Для всех остальных запросов требуется аутентификация
        return request.user.is_authenticated


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает изменять данные только владельцу объекта.
    """

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем
        if request.method in SAFE_METHODS:
            return True
        # Запись разрешена только владельцу
        return obj == request.user

class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает изменение только владельцу объекта, для остальных - только чтение.
    """
    def has_object_permission(self, request, view, obj):
        # Если пользователь не авторизован, возвращаем 401
        if request.user.is_anonymous:
            return False
        # Если метод чтения (GET, HEAD, OPTIONS), то разрешаем
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Если метод изменения (PUT, PATCH, DELETE), разрешаем только владельцу
        return obj.author == request.user