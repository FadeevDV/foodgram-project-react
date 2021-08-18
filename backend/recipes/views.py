from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import Ingredient, Tag, Recipe
from .serializers import (IngredientSerializer, TagSerializer,
                          RecipeSerializer_NOTSAFE, RecipeSerializer_SAFE)
from users.permissions import IsAdminOrReadOnly


class IngredientViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """Операции с Ingredient"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def delete(self, request, slug):
        ingredient = get_object_or_404(Ingredient, slug=slug)
        ingredient.delete()
        return Response(status.HTTP_200_OK, status=status.HTTP_204_NO_CONTENT)


class TagViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """Операции с Тегами"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def delete(self, request, slug):
        tag = get_object_or_404(Tag, slug=slug)
        tag.delete()
        return Response(status.HTTP_200_OK, status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    """Операции с рецептами"""
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        safe_methods = ['list', 'retrieve']
        print(self.action)
        if self.action in safe_methods:
            return RecipeSerializer_SAFE
        return RecipeSerializer_NOTSAFE
