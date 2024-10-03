from django_filters.rest_framework import FilterSet, filters

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    """Список фильтров для рецептов."""
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug', to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_filter')

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

    def filter_is_favorited(self, queryset, name, value):
        """Возвращает рецепты по фильтру "в избранном"."""
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        """Возвращает рецепты по фильтру "в списке покупок"."""
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
