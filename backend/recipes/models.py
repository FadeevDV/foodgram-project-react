from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Ингредиент'
    )
    slug = models.SlugField(
        null=False,
        blank=False,
        unique=True,
        verbose_name='slug ингредиентов рецепта'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Tag(models.Model):
    name = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Тег'
    )
    slug = models.SlugField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
        verbose_name='slug Тега'
    )
    color = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    """Модель рецепта."""
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='Рецепт блюда'
    )
    Cooking_time = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name='Время приготовления'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Рейтинг не может быть ниже 1'),
            MaxValueValidator(5, 'Рейтинг не может быть выше 5'),
        ],
        null=True,
        verbose_name="Рейтинг",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание рецепта'
    )
    tag = models.ManyToManyField(
        Tag,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        null=True,
        on_delete=models.SET_NULL,
        related_name='ingredient'
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class IngredientItem(models.Model):
    """Модель Ингредиента с кол-вом для модели Рецепта"""

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    count = models.DecimalField(
        verbose_name="кол-во", max_digits=6, decimal_places=1
    )

    class Meta:
        verbose_name = "Ингредиент из рецепта"
        verbose_name_plural = "Ингредиенты из рецептов"

    def __str__(self):
        return (
            f"{self.ingredient.title} - {self.count} "
            f"{self.ingredient.dimension}"
        )


class Favorites(models.Model):
    """модель Избранного"""

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="fans"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites"
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"


class Subscribe(models.Model):
    """модель Подписки"""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscribers"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscribes"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class ShopListItem(models.Model):
    """модель Списка покупок"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shop_list"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="to_buy"
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"



