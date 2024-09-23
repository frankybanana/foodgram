from django.contrib.auth import get_user_model
from recipes.models import (FavoriteRecipe,
                            Ingredient,
                            Recipe,
                            RecipeIngredient,
                            ShoppingCart,
                            Tag)


User = get_user_model()