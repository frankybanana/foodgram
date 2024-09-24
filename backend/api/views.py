from django.contrib.auth import get_user_model
from rest_framework import viewsets
from djoser.views import UserViewSet as DjoserUserViewSet

from recipes.models import (FavoriteRecipe,
                            Ingredient,
                            Recipe,
                            RecipeIngredient,
                            ShoppingCart,
                            Tag)

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    pass


class TagViewSet(viewsets.ModelViewSet):
    pass


class IngredientViewSet(viewsets.ModelViewSet):
    pass


class RecipeViewSet(viewsets.ModelViewSet):
    pass




