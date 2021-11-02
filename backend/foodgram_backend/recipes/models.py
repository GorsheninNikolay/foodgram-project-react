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

    class Meta:
        ordering = ['id', ]


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название', unique=True
        )
    measurment_unit = models.CharField(
        max_length=200, verbose_name='Единицы измерения'
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id', ]


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               related_name='recepts',
                               null=True, verbose_name='Автор публикации')
    name = models.CharField(
        max_length=200, verbose_name='Название'
        )
    image = models.ImageField(
        upload_to='images/', verbose_name='Картинка'
        )
    text = models.TextField(verbose_name='Описание')
    tags = models.ManyToManyField(Tag, related_name='tags')
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient', related_name='recepts'
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(
            1, message='Время приготовления больше минуты'
        )],
        verbose_name='Время приготовления в минутах')

    def ingredients_set(self):
        return RecipeIngredient.objects.filter(recipe=self)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id', ]


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
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
        return '%s: %d' % (self.ingredient.name, self.amount)


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Время публикации',
                                    auto_now_add=True)

    class Meta:
        ordering = ['-pub_date', ]
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='unique_favorite'
            ),
        ]


class ShoppingCart(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'recipe'], name='unique_shoppingcart'
            )
        ]
