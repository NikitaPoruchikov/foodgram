from rest_framework import viewsets
from django.contrib.auth import get_user_model
from api.serializers import UserCreateSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
