from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsAuthenticatedForFilter(permissions.BasePermission):
    """
    Разрешает доступ к рецептам только для авторизованных пользователей.
    """

    def has_permission(self, request, view):
        filter_params = ["is_favorited", "is_in_shopping_cart"]

        if not any(param in request.query_params for param in filter_params):
            return True

        return request.user and request.user.is_authenticated


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
