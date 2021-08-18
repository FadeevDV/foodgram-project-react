from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, TagViewSet, RecipeViewSet

# создаем роутер
v1_router = DefaultRouter()

v1_router.register(
    r'recipes',
    IngredientViewSet,
    basename='recipes'
)

v1_router.register(
    r'Tag',
    TagViewSet,
    basename='recipes'
)

v1_router.register(
    r'titles',
    RecipeViewSet,
    basename='titles'
)




urlpatterns = [
    path('', include(v1_router.urls)),
]
