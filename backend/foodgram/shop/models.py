from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe


User = get_user_model()


class ShoppingCart(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart')

    recipes = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт в корзине',
        related_name='customers',
        on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipes'],
                name='unique_user_recipe_from_shop'
            )
        ]
