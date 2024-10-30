from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models

from api.constants import (MAX_LENGTH_FIRST_NAME, MAX_LENGTH_LAST_NAME,
                           MAX_LENGTH_USERNAME, USERNAME_REGEX,
                           USERNAME_VALIDATION_ERROR)


class UserRole:
    USER = "user"
    ADMIN = "admin"
    choices = [(USER, "USER"), (ADMIN, "ADMIN")]


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message=USERNAME_VALIDATION_ERROR)
        ],
    )
    first_name = models.CharField(max_length=MAX_LENGTH_FIRST_NAME)
    last_name = models.CharField(max_length=MAX_LENGTH_LAST_NAME)
    role = models.TextField(
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name="Пользовательская роль",
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = UserManager()

    class Meta:
        ordering = ("id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
