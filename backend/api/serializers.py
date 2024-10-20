from rest_framework import serializers
from .models import Recipe, Ingredient, Tag, RecipeIngredient, Subscription, ShoppingCart, Favorite
from drf_extra_fields.fields import Base64ImageField
from users.models import CustomUser
import logging
from django.core.validators import RegexValidator
from rest_framework.exceptions import ValidationError


logging.basicConfig(level=logging.INFO)


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = CustomUser
        fields = ['avatar']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z', message="Введите правильное имя пользователя. Оно может содержать только буквы, цифры и символы @/./+/-/_.")]
    )


    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        ]

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise ValidationError("Пользователь с таким username уже существует.")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return value

    def create(self, validated_data):
        logging.info(f"Creating user with email: {validated_data['email']}")

        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])  # Хешируем пароль
        user.save()  # Сохраняем пользователя в базу данных

        logging.info(f"User created with hashed password: {user.password}")
        return user


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()


    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'avatar', 'is_subscribed']


    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, author=obj).exists()

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)
        return None


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
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
    
    @staticmethod
    def validate_amount(value):
        """Метод валидации количества"""

        if value < 1:
            raise serializers.ValidationError(
                'Количество ингредиента должно быть больше 0!'
            )
        return value


# Сериализатор для отображения ингредиентов в рецепте
class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit")
    amount = serializers.ReadOnlyField()

    class Meta:
        model = RecipeIngredient
        fields = ["id", "name", "measurement_unit", "amount"]
        
class SubscriptionRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientWriteSerializer(many=True, write_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            "id", "tags", "author", "ingredients", "is_favorited",
            "is_in_shopping_cart", "name", "image", "text", "cooking_time",
        ]

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_cart__user=user)
        elif not value and user.is_authenticated:
            return queryset.exclude(shopping_cart__user=user)
        return queryset

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        # Проверяем параметр запроса is_in_shopping_cart
        is_in_shopping_cart = self.request.query_params.get('is_in_shopping_cart')
        if is_in_shopping_cart is not None and user.is_authenticated:
            if is_in_shopping_cart == '1':
                queryset = queryset.filter(shopping_cart__user=user)
            elif is_in_shopping_cart == '0':
                queryset = queryset.exclude(shopping_cart__user=user)

        return queryset

    # Валидация времени готовки
    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError("Время готовки не может быть меньше 1.")
        return value

    # Валидация изображения
    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError("Изображение не может быть пустым.")
        return value

    # Валидация тегов (убрал проверку на уникальность внутри одного списка)
    def validate_tags(self, value):
        
        if len(value) == 0:
            raise serializers.ValidationError("Необходимо выбрать хотя бы один тег.")

        unique_tags = set(value)
        if len(unique_tags) != len(value):
            raise serializers.ValidationError("Теги не могут повторяться.")
    
        return value

    # Валидация ингредиентов (обязательное наличие и проверка дубликатов)
    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError("Список ингредиентов не может быть пустым.")
        ingredient_ids = [item['ingredient'].id for item in value]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError("Ингредиенты не могут повторяться.")
        return value

    # Преобразование данных при возврате ответа
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["tags"] = TagSerializer(instance.tags.all(), many=True).data
        representation["ingredients"] = RecipeIngredientReadSerializer(instance.recipe_ingredients.all(), many=True).data
        return representation

    # Создание рецепта
    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients_data = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients_data)
        return recipe

    # Обновление ингредиентов
    def create_ingredients(self, recipe, ingredients_data):
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient_data['ingredient'],
                amount=ingredient_data['amount'],
            ) for ingredient_data in ingredients_data
        ])

    # Обновление рецепта
    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        ingredients_data = validated_data.pop("ingredients", None)

        # Обновляем теги, если они переданы
        if tags is not None:
            instance.tags.set(tags)

        # Обновляем ингредиенты, если они переданы
        if ingredients_data is not None:
            instance.recipe_ingredients.all().delete()
            self.create_ingredients(instance, ingredients_data)

        # Обновляем другие поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(user=user, recipe=obj).exists()
        return False