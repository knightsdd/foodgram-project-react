# Generated by Django 2.2.19 on 2022-02-02 07:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220131_1319'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='recipes',
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='recipes',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='recipes.Recipe', verbose_name='Рецепты в корзине'),
        ),
    ]
