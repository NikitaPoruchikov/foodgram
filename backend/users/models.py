from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=255,
        unique=True
    )
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to='avatars/',
        blank=True,
        null=True
    )
    is_subscribed = models.BooleanField(
        verbose_name="Подписан ли пользователь",
        default=False
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
