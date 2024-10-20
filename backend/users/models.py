# users/models.py
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class UserRole:
    USER = 'user'
    ADMIN = 'admin'
    choices = [
        (USER, 'USER'),
        (ADMIN, 'ADMIN')
    ]


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True)
    username = models.CharField(
        max_length=150, unique=True)
    first_name = models.CharField(
        max_length=150)
    last_name = models.CharField(
        max_length=150)
    role = models.TextField(
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name="Пользовательская роль",
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = UserManager()

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
