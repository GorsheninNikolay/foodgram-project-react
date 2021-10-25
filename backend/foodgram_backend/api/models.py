from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               related_name='recepts',
                               null=True, verbose_name='Автор публикации')
    name = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(verbose_name='Картинка')
    text = models.TextField(verbose_name='Описание')
    tag = models.SlugField(verbose_name='Тег')
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(
            1, message='Время приготовления больше минуты'
        )],
        verbose_name='Время приготовления в минутах')


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    measurment_unit = models.CharField(
        max_length=200, verbose_name='Единицы измерения'
        )
    amount = models.IntegerField(
        validators=[MinValueValidator(
            1, message='Количество ингридиентов не может быть ниже 1')],
        verbose_name='Количество'
        )


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    color = models.CharField(default='#49B64E', max_length=7,
                             verbose_name='Цветовой HEX-код')
    slug = models.SlugField(related_name='tags')
