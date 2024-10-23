from django.db import models
from django.contrib.auth import get_user_model

from users.models import CustomUser
from .constants import MAX_LENGTH, MAX_LENGTH_UNIT


# Модель Тегов
class Tag(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    slug = models.SlugField(max_length=MAX_LENGTH, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


# Модель Ингредиентов
class Ingredient(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    measurement_unit = models.CharField(max_length=MAX_LENGTH_UNIT)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        unique_together = ["name", "measurement_unit"]

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"


# Модель Рецептов
class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="recipes"
    )
    name = models.CharField(max_length=MAX_LENGTH)
    image = models.ImageField(
        upload_to="recipes/images/", blank=True, null=True)
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient")
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


# Промежуточная модель для связи рецептов и ингредиентов
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецептов"
        unique_together = ["recipe", "ingredient"]


# Модель для подписок
class Subscription(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        related_name="subscriptions"
    )
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        related_name="subscribers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ["user", "author"]

    def __str__(self):
        return f"{self.user.username} подписан на {self.author.username}"


# Модель для избранного
class Favorite(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        related_name="favorites"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name="favorited_by"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        unique_together = ["user", "recipe"]

    def __str__(self):
        return f"{self.user.username} добавил в избранное {self.recipe.name}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name="shopping_cart"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name="in_cart")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_shopping_cart"
            )
        ]
        verbose_name = "Корзина покупок"
        verbose_name_plural = "Корзины покупок"

    def __str__(self):
        return f"{self.user} - {self.recipe}"
