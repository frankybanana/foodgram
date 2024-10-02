from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    TagsViewSet, IngredientsViewSet, RecipesViewSet, CustomUserViewSet
)

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('users/me/avatar', CustomUserViewSet, basename='avatar')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
