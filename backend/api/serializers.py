from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from api.fields import Base64ImageField
from backend.constants import MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH
from recipes.models import (Favorite,
                            Ingredient,
                            Recipe,
                            RecipeIngredient,
                            ShoppingCart,
                            Tag)
from users.models import Follow

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    email = serializers.EmailField(required=True,
                                   max_length=MAX_EMAIL_LENGTH)
    first_name = serializers.CharField(required=True,
                                       max_length=MAX_USERNAME_LENGTH)
    last_name = serializers.CharField(required=True,
                                      max_length=MAX_USERNAME_LENGTH)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    avatar = Base64ImageField(required=False, allow_null=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'avatar',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Проверяет подписку текущего пользователя на объект запроса."""
        return (
            self.context.get('request').user.is_authenticated
            and Follow.objects.filter(
                follower=self.context.get('request').user,
                author=obj.id
            ).exists()
        )


class CustomUserAvatarSerializer(UserSerializer):
    """Сериализатор для аватара пользователя."""

    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = (
            'avatar',
        )


class FollowSerializer(CustomUserSerializer):
    """Сериализатор пользователей, на которых подписан текущий юзер."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'id',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar'
        )

    def validate(self, data):
        author = data.get('author')
        follower = self.context.get('request').user
        if follower == author:
            raise ValidationError(
                detail='Вы не можете подписаться на самого себя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes(self, obj):
        """Возращает рецепты согласно параметру "recipes_limit" в запросе."""
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.id)
        if limit:
            recipes = recipes[:int(limit)]
        serializer = ShortRecipeSerializer(recipes, many=True, read_only=True)
        return serializer.data

    def get_recipes_count(self, obj):
        """
        Подсчитывает кол-во рецептов у пользователя,
        на которого подписан юзер.
        """
        return Recipe.objects.filter(author=obj.id).count()


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipesIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для связи рецептов и ингредиентов."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра рецептов."""

    author = CustomUserSerializer(read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    ingredients = RecipesIngredientsSerializer(
        many=True, read_only=True, source='recipe_ingredient')

    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    def get_is_favorited(self, obj):
        """Проверяет, есть ли рецепт в избранном."""
        return (
            self.context.get('request').user.is_authenticated
            and Favorite.objects.filter(
                user=self.context.get('request').user,
                recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """Проверяет, есть ли рецепт в списке покупок."""
        return (
            self.context.get('request').user.is_authenticated
            and ShoppingCart.objects.filter(
                user=self.context.get('request').user,
                recipe=obj
            ).exists()
        )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )


class CreateRecipesIngredientsSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для связи рецептов и ингредиентов."""
    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class CreateRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецептов."""

    author = CustomUserSerializer(read_only=True)
    ingredients = CreateRecipesIngredientsSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField(required=True, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author'
        )

    def validate(self, data):
        """Проверяет поля тегов и ингредиентов."""
        if not data.get('ingredients'):
            raise ValidationError('Нужно добавить хотя бы один ингредиент!')
        if not data.get('tags'):
            raise ValidationError('Нужно добавить хотя бы один тег!')

        ingredients_list = data['ingredients']
        ingredients = []

        for ingredient in ingredients_list:
            if not Ingredient.objects.filter(id=ingredient['id']).exists():
                raise ValidationError('Такого ингредиента нет!')
            ingredients.append(ingredient['id'])
            if ingredients.count(ingredient['id']) > 1:
                raise ValidationError(
                    'Нельзя включать два одинаковых ингредиента!'
                )

        tags_list = data['tags']
        tags = []
        for tag in tags_list:
            if tag in tags:
                raise ValidationError('Нельзя указать два одинаковых тега!')
            tags.append(tag)
        return data

    def bulk_create_update(self, ingredients, recipe):
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_list.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient_id=ingredient.get('id'),
                    amount=ingredient.get('amount')
                )
            )
        RecipeIngredient.objects.bulk_create(ingredient_list)

    def create(self, validated_data):
        """Создание рецепта."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.bulk_create_update(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Редактирование рецепта."""
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        self.bulk_create_update(ingredients, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipesSerializer(instance, context=self.context).data


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для краткого отображения рецептов."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
