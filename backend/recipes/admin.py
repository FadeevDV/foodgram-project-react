from django.contrib import admin

from .models import Ingredient, Tag, Recipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('slug',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('slug',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'Cooking_time', 'rating', 'description'
    )
    search_fields = ('name',)
    list_filter = ('Cooking_time',)
    empty_value_display = '-пусто-'


class ShopListAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    list_filter = ("user",)
    search_fields = ("recipe",)


class IngredientItem(admin.ModelAdmin):
    list_display = ("ingredient", "count")


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
