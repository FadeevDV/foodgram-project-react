from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        help_text='Введите название тега',
        max_length=200,
        unique=True,
    )
    color = ColorField(
        verbose_name='Цвет в HEX',
        help_text='Введите цвет тега в HEX',
        unique=True,
        null=True,
    )
    slug = models.CharField(
        verbose_name='Уникальный слаг',
        help_text='Введите уникальный слаг',
        max_length=200,
        unique=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения',
        help_text='Выберите единицу измерения',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=50, verbose_name='Название рецепта'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        help_text='Выберите изображение'
    )
    text = models.TextField(
        max_length=1000, verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientForRecipe',
        verbose_name='Ингредиенты',
        help_text='Укажите ингредиенты и их количество',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления', default=1,
        validators=[MinValueValidator(1, 'Значение не может быть меньше 1')]
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        help_text='Выберите один или несколько тегов'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientForRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_amounts',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_amounts',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество', default=1,
        validators=[MinValueValidator(1, 'Значение не может быть меньше 1')]
    )

    class Meta:
        verbose_name = 'Количество ингредиента в рецепте'

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite',
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.user}'


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.user}'
