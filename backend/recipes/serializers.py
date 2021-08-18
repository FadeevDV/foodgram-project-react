from rest_framework import serializers

from .models import Ingredient, Tag, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug', )
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug', )
        model = Tag


class RecipeSerializer_SAFE(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'cooking_time', 'rating', 'description', 'tag', 'ingredient'
        )
        model = Recipe


class RecipeSerializer_NOTSAFE(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='slug',
        many=True
    )
    ingredient = serializers.SlugRelatedField(
        queryset=Ingredient.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = (
            'id', 'name', 'cooking_time', 'rating', 'description', 'tag', 'ingredient'
        )
        model = Recipe
