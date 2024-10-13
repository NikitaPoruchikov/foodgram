from rest_framework import serializers
from .models import Recipe, Ingredient, Tag, RecipeIngredient
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth import get_user_model
from users.models import CustomUser

from django.db import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "avatar",
        ]

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return user.subscriptions.filter(author=obj).exists()


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name"]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "measurement_unit"]


# Сериализатор для создания ингредиентов в рецепте
class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source="ingredient"
    )

    class Meta:
        model = RecipeIngredient
        fields = ["id", "amount"]


# Сериализатор для отображения ингредиентов в рецепте
class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(source="ingredient.measurement_unit")
    amount = serializers.ReadOnlyField()

    class Meta:
        model = RecipeIngredient
        fields = ["id", "name", "measurement_unit", "amount"]


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    author = AuthorSerializer(read_only=True)
    ingredients = RecipeIngredientWriteSerializer(many=True, write_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["tags"] = TagSerializer(instance.tags.all(), many=True).data
        representation["ingredients"] = RecipeIngredientReadSerializer(
            instance.recipe_ingredients.all(), many=True
        ).data
        return representation

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients_data = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients_data)
        return recipe

    def create_ingredients(self, recipe, ingredients_data):
        RecipeIngredient.objects.bulk_create(
            [
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient_data[
                        "ingredient"
                    ],  # Теперь это работает правильно
                    amount=ingredient_data["amount"],
                )
                for ingredient_data in ingredients_data
            ]
        )

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        ingredients_data = validated_data.pop("ingredients", None)

        if tags is not None:
            instance.tags.set(tags)

        if ingredients_data is not None:
            instance.recipe_ingredients.all().delete()
            self.create_ingredients(instance, ingredients_data)

        return super().update(instance, validated_data)

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False
