# Generated by Django 2.2.19 on 2022-02-04 16:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20220202_1300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'ordering': ['-pk'], 'verbose_name': 'Избранный рецепт', 'verbose_name_plural': 'Избранные рецепты'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name'], 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='ingredientforrecipe',
            options={'ordering': ['-pk'], 'verbose_name': 'Ингредиент для рецепта', 'verbose_name_plural': 'Ингредиенты для рецептов'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fan', to='recipes.Recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fav_recipes', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
