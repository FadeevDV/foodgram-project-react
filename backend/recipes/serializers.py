from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer

from .models import (Favorites, Ingredient, IngredientForRecipe, Purchase,
                     Recipe, Tag)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    recipe = serializers.IntegerField(source='recipe.id')

    class Meta:
        model = Favorites
        fields = ['user', 'recipe']

    def validate(self, data):
        user = data['user']['id']
        recipe = data['recipe']['id']
        if Favorites.objects.filter(user=user, recipe__id=recipe).exists():
            raise serializers.ValidationError(
                {
                    "errors": "Нельзя добавить повторно в избранное"
                }
            )
        return data

    def create(self, validated_data):
        user = validated_data["user"]
        recipe = validated_data["recipe"]
        Favorites.objects.get_or_create(user=user, recipe=recipe)
        return validated_data


class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    recipe = serializers.IntegerField(source='recipe.id')

    class Meta:
        model = Purchase
        fields = '__all__'

    def validate(self, data):
        user = data['user']['id']
        recipe = data['recipe']['id']
        if Purchase.objects.filter(user=user, recipe__id=recipe).exists():
            raise serializers.ValidationError(
                {
                    "errors": "Вы уже добавили рецепт в корзину"
                }
            )
        return data

    def create(self, validated_data):
        user = validated_data["user"]
        recipe = validated_data["recipe"]
        Purchase.objects.get_or_create(user=user, recipe=recipe)
        return validated_data


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField()

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = IngredientForRecipe
        fields = ['id', 'name', 'amount', 'measurement_unit']


class IngredientForRecipeCreate(IngredientForRecipeSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    def validate_amount(self, amount):
        if amount < 1:
            raise serializers.ValidationError(
                'Убедитесь, что это значение больше 0.'
            )
        return amount

    def to_representation(self, instance):
        ingredient_in_recipe = [
            item for item in
            IngredientForRecipe.objects.filter(ingredient=instance)
        ]
        return IngredientForRecipeSerializer(ingredient_in_recipe).data


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientForRecipeCreate(many=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text',
            'cooking_time', 'pub_date'
        ]

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorites.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Purchase.objects.filter(user=request.user, recipe=obj).exists()

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags_data)
        for ingredient in ingredients:
            amount = ingredient.get('amount')
            ingredient_instance = get_object_or_404(Ingredient,
                                                    pk=ingredient.get('id'))
            IngredientForRecipe.objects.create(recipe=recipe,
                                               ingredient=ingredient_instance,
                                               amount=amount)
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.filter(id=instance.id)
        recipe.update(**validated_data)
        ingredients_instance = [
            ingredient for ingredient in instance.ingredients.all()
        ]
        for item in ingredients_data:
            amount = item['amount']
            ingredient_id = item['id']
            if IngredientForRecipe.objects.filter(
                    id=ingredient_id, amount=amount
            ).exists():
                ingredients_instance.remove(
                    IngredientForRecipe.objects.get(id=ingredient_id,
                                                    amount=amount
                                                    ).ingredient)
            else:
                IngredientForRecipe.objects.get_or_create(
                    recipe=instance,
                    ingredient=get_object_or_404(Ingredient, id=ingredient_id),
                    amount=amount
                )
        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image', instance.image)
        instance.ingredients.remove(*ingredients_instance)
        instance.tags.set(tags_data)
        return instance


class RecipeReadSerializer(RecipeSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        ingredients = IngredientForRecipe.objects.filter(recipe=obj)
        return IngredientForRecipeSerializer(ingredients, many=True).data
