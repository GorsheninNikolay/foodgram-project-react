# Generated by Django 3.2.8 on 2021-11-03 18:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20211103_2116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Избранные'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'ordering': ['-id'], 'verbose_name': 'Ингредиент рецепта', 'verbose_name_plural': 'Ингредиенты рецепта'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'Спиок покупок'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Время приготовления должно быть больше минуты')], verbose_name='Время приготовления в минутах'),
        ),
    ]