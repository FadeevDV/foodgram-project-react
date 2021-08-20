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
        verbose_name='Уникальный slag',
        help_text='Введите уникальный slag',
        max_length=200,
        unique=True,
        null=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Ингредиент',
        help_text='Введите название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=10,
        verbose_name='Единица измерения',
        help_text='Выберите единицу измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        help_text='Выберите изображение'
    )
    description = models.TextField(
        max_length=1000,
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientItem',
        verbose_name='Ингредиенты',
        help_text='Укажите ингредиенты и их количество',
    )
    cooking_time = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1, 'Значение не может быть меньше 1')],
        null=False,
        blank=False,
        verbose_name='Время приготовления'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        help_text='Выберите один или несколько тегов',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientItem(models.Model):
    """Модель Ингредиента с кол-вом для модели Рецепта"""

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
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты из рецептов'

    def __str__(self):
        return (
            f'{self.ingredient} в {self.recipe}'
        )


class Favorites(models.Model):
    """модель Избранного"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='fans'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Subscribe(models.Model):
    """модель Подписки"""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscribers'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscribes'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class ShopListItem(models.Model):
    """модель Списка покупок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shop_list'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='to_buy'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ['-pub_date']

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.user}'
