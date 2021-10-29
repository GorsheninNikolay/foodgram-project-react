from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    color = models.CharField(default='#49B64E', max_length=7,
                             verbose_name='Цветовой HEX-код')
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название', unique=True
        )
    measurment_unit = models.CharField(
        max_length=200, verbose_name='Единицы измерения'
        )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               related_name='recepts',
                               null=True, verbose_name='Автор публикации')
    name = models.CharField(
        max_length=200, unique=True, verbose_name='Название'
        )
    image = models.ImageField(
        upload_to='images/', verbose_name='Картинка'
        )
    text = models.TextField(verbose_name='Описание')
    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient'
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(
            1, message='Время приготовления больше минуты'
        )],
        verbose_name='Время приготовления в минутах')

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    name = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE
        )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(
            1, message='Количество ингридиентов не может быть ниже 1')],
        default=1,
        verbose_name='Количество'
        )

    def __str__(self):
        return '%s: %d' % (self.name, self.amount)


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published',
                                    auto_now_add=True)

    class Meta:
        ordering = ['-pub_date', ]
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='unique_favorite'
            ),
        ]
