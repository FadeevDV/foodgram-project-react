from django_filters import rest_framework as filters

from .models import Recipe


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class RecipeFilter(filters.FilterSet):
    ingredient = CharFilterInFilter(
        field_name='ingredient__slug',
        lookup_expr='in',
    )
    Tag = CharFilterInFilter(
        field_name='tag__slug',
        lookup_expr='in',

    )
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='contains',
    )

    class Meta:
        model = Recipe
        fields = (
            'tag',
            'ingredient',
            'Cooking_time',
            'name',
        )
