from django.db import models


class Tag(models.Model):

    name = models.CharField(
        max_length=20,
        verbose_name='Название')

    color = models.CharField(
        max_length=7,
        default='#ffffff',
        verbose_name='Цветовой Hex-код')

    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальное имя slug')

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['slug']
