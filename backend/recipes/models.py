from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from backend.constants import (
    MAX_AMOUNT_INGREDIENTS,
    MAX_COOKING_TIME,
    MAX_NAME_LENGTH,
    MAX_TAG_LENGTH,
    MAX_SLUG_LENGTH,
    MAX_UNIT_LENGTH,
    MIN_AMOUNT_INGREDIENTS,
    MIN_COOKING_TIME,
)

User = get_user_model()


class Ingredient(models.Model):

    name = models.CharField(max_length=MAX_NAME_LENGTH,
                            verbose_name='Ингредиент')
    measurement_unit = models.CharField(max_length=MAX_UNIT_LENGTH,
                                        verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        unique_together = ('name', 'measurement_unit')

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(max_length=MAX_TAG_LENGTH,
                            verbose_name='Тег')
    slug = models.CharField(max_length=MAX_SLUG_LENGTH,
                            verbose_name='Слаг')

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)
        unique_together = ('name', 'slug')

    def __str__(self):
        return self.name


class Recipe(models.Model):

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиент',
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=True, null=True,
        default=None,
        verbose_name='Изображение'
    )
    name = models.CharField('Название', max_length=200)
    text = models.TextField('Описание')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                message=(
                    'Минимальное время приготовления '
                    f'не может быть меньше {MIN_COOKING_TIME}'
                ),
            ),
            MaxValueValidator(
                MAX_COOKING_TIME,
                message=(
                    'Максимальное время приготовления '
                    f'не может быть больше {MAX_COOKING_TIME}'
                ),
            )
        ],
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Ингредиент',
    )
    amount = models.IntegerField(
        verbose_name="Количество",
        validators=(
            MinValueValidator(
                MIN_AMOUNT_INGREDIENTS,
                message=(
                    'Количество ингредиента не может быть '
                    f'меньше {MIN_AMOUNT_INGREDIENTS}'
                ),
            ),
            MaxValueValidator(
                MAX_AMOUNT_INGREDIENTS,
                message=(
                    'Количество ингредиента не может быть '
                    f'больше {MAX_AMOUNT_INGREDIENTS}'
                ),
            )
        ),
    )

    class Meta:
        default_related_name = 'recipe_ingredient'
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.ingredient} {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.user}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'Списки покупок'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_shopping_cart'
            )
        ]

    def __str__(self):
        return f'У {self.user.username} в корзине {self.recipe.name}'
