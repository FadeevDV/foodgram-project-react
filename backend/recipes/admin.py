from django.contrib import admin
from import_export.admin import ImportMixin


from .models import Favorites, Ingredient, IngredientItem, Recipe, Tag
from .resources import IngredientResource


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')


class IngredientItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'name',
    )
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'


class IngredientAdmin(ImportMixin, admin.ModelAdmin):
    list_filter = ('id', 'name', 'measurement_unit',)
    search_fields = ('name',)
    resource_class = IngredientResource


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


admin.site.register(IngredientItem, IngredientItemAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorites, FavoriteAdmin)
