from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipesViewSet, ShoppingCartView,
                    TagsViewSet, download_shopping_cart)

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingCartView.as_view(),
         name='shopping_cart'),
    path('recipes/download_shopping_cart/', download_shopping_cart,
         name='download_shopping_cart'),
    path('', include(router.urls)),
]
