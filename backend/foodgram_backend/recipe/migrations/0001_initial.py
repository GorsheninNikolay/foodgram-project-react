# Generated by Django 3.2.8 on 2021-10-28 13:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
                ('measurment_unit', models.CharField(max_length=200, verbose_name='Единицы измерения')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('image', models.ImageField(upload_to='', verbose_name='Картинка')),
                ('text', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Время приготовления больше минуты')], verbose_name='Время приготовления в минутах')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('color', models.CharField(default='#49B64E', max_length=7, verbose_name='Цветовой HEX-код')),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Количество ингридиентов не может быть ниже 1')], verbose_name='Количество')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.recipe')),
            ],
        ),
    ]