from functools import wraps

from rest_framework.response import Response
from rest_framework import status


def author_required(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Необходима авторизация."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if obj.author != request.user:
            return Response(
                {"detail": "У вас нет прав на выполнение этого действия."},
                status=status.HTTP_403_FORBIDDEN
            )
        return view_func(self, request, *args, **kwargs)
    return _wrapped_view
