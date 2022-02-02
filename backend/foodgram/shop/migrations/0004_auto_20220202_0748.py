# Generated by Django 2.2.19 on 2022-02-02 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20220202_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='recipes.Recipe', verbose_name='Рецепт в корзине'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipes'), name='unique_user_recipe_from_shop'),
        ),
    ]
