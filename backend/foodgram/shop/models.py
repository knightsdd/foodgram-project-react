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

    recipes = models.ManyToManyField(
        Recipe,
        verbose_name='Рецепты в корзине')
