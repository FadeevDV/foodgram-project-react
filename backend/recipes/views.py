import django_filters.rest_framework
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import RecipeSubscriptionSerializer

from .filters import IngredientNameFilter, RecipeFilter
from .models import (Favorites, Ingredient, IngredientItem, Recipe,
                     ShopListItem, Tag)
from .permissions import AdminOrAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer_NOTSAFE, RecipeSerializer_SAFE,
                          ShopListItemSerializer, TagSerializer)

User = get_user_model()


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_class = RecipeFilter
    pagination_class = PageNumberPagination
    permission_classes = [AdminOrAuthorOrReadOnly, ]

    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_in_shopping_cart = self.request.query_params.get(
            "is_in_shopping_cart"
        )
        is_favorited = self.request.query_params.get("is_favorited")
        cart = ShopListItem.objects.filter(user=self.request.user.id)
        favorite = Favorites.objects.filter(user=self.request.user.id)

        if is_in_shopping_cart == "true":
            queryset = queryset.filter(purchase__in=cart)
        elif is_in_shopping_cart == "false":
            queryset = queryset.exclude(purchase__in=cart)
        if is_favorited == "true":
            queryset = queryset.filter(favorites__in=favorite)
        elif is_favorited == "false":
            queryset = queryset.exclude(favorites__in=favorite)
        return queryset.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return RecipeSerializer_NOTSAFE
        return RecipeSerializer_SAFE

    @action(methods=["GET", "DELETE"],
            url_path='favorite', url_name='favorite',
            permission_classes=[permissions.IsAuthenticated], detail=True)
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = FavoriteSerializer(
            data={'user': request.user.id, 'recipe': recipe.id}
        )
        if request.method == "GET":
            serializer.is_valid(raise_exception=True)
            serializer.save(recipe=recipe, user=request.user)
            serializer = RecipeSubscriptionSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = get_object_or_404(
            Favorites, user=request.user, recipe__id=pk
        )
        favorite.delete()
        return Response(
            f'Рецепт {favorite.recipe} удален из избранного у пользователя '
            f'{request.user}', status=status.HTTP_204_NO_CONTENT
        )


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny, )
    pagination_class = None
    filterset_class = IngredientNameFilter


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def download_shopping_cart(request):
    user = request.user
    cart = user.purchase_set.all()
    buying_list = {}
    for item in cart:
        recipe = item.recipe
        ingredients_in_recipe = IngredientItem.objects.filter(
            recipe=recipe
        )
        for item in ingredients_in_recipe:
            amount = item.amount
            name = item.ingredient.name
            measurement_unit = item.ingredient.measurement_unit
            if name not in buying_list:
                buying_list[name] = {
                    'amount': amount,
                    'measurement_unit': measurement_unit
                }
            else:
                buying_list[name]['amount'] = (
                    buying_list[name]['amount'] + amount
                )
    shopping_list = []
    for item in buying_list:
        shopping_list.append(
            f'{item} - {buying_list[item]["amount"]}, '
            f'{buying_list[item]["measurement_unit"]}\n'
        )
    response = HttpResponse(shopping_list, 'Content-Type: text/plain')
    response['Content-Disposition'] = (
        'attachment;' 'filename="shopping_list.txt"'
    )
    return response


class ShoppingCartView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'delete']

    def get(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer = ShopListItemSerializer(
            data={'user': user.id, 'recipe': recipe.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(recipe=recipe, user=request.user)
        serializer = RecipeSubscriptionSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        cart = get_object_or_404(ShopListItem, user=user, recipe__id=recipe_id)
        cart.delete()
        return Response(
            f'Рецепт {cart.recipe} удален из корзины у пользователя {user}, '
            f'status=status.HTTP_204_NO_CONTENT'
        )
