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
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название'
        )
    measurement_unit = models.CharField(
        max_length=200, verbose_name='Единицы измерения'
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id', ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True, verbose_name='Автор публикации')
    name = models.CharField(
        max_length=200, unique=True, verbose_name='Название'
        )
    image = models.FileField(upload_to='images/', verbose_name='Картинка')
    text = models.TextField(verbose_name='Описание')
    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient'
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(
            1, message='Время приготовления должно быть больше минуты'
        )],
        verbose_name='Время приготовления в минутах')

    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)

    def ingredients_set(self):
        return RecipeIngredient.objects.filter(recipe=self)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id', ]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


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

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Время публикации',
                                    auto_now_add=True)

    class Meta:
        ordering = ['-pub_date', ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='unique_favorite'
            ),
        ]


class ShoppingCart(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Спиок покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'recipe'], name='unique_shoppingcart'
            )
        ]
