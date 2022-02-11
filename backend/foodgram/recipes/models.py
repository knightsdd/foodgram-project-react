from django.contrib.auth import get_user_model
from django.db import models
from tags.models import Tag

User = get_user_model()


class Ingredient(models.Model):

    name = models.CharField(
        max_length=150,
        verbose_name='Название продукта')

    measurement_unit = models.CharField(
        max_length=10,
        verbose_name='Единицы измерения')

    def __str__(self) -> str:
        return f'{self.name}, ({self.measurement_unit})'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта')

    name = models.CharField(
        max_length=200,
        verbose_name='Название')

    text = models.TextField(
        verbose_name='Описание рецепта')

    image = models.ImageField(
        verbose_name='Изображение')

    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
        )

    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах')

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации рецепта')

    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиенты',
        through='IngredientForRecipe')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.name[:25]


class IngredientForRecipe(models.Model):

    ingredient = models.ForeignKey(
        Ingredient,
        related_name='amounts',
        on_delete=models.CASCADE,
        verbose_name='Ингредиент')

    recipe = models.ForeignKey(
        Recipe,
        related_name='ings_for_recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт')

    amount = models.PositiveIntegerField(
        verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецептов'
        ordering = ['-pk']

    def __str__(self):
        return f'{self.ingredient} - {self.recipe} - {self.amount}'


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='fav_recipes')

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='fan')

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} likes {self.recipe}'
