from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )
    fieldsets = [
        (None, {'fields': ['author', 'name', 'image',
                           'text', 'tags', 'cooking_time']}),
    ]
    list_display = ('id', 'name', 'author', )
    list_filter = ('author', 'name', 'tags', )

    def save_model(self, request, obj, form, change):
        """Чтобы nginx по имени рецепта нашел картинку,
        динамически переименовываю файл"""
        image_name, image_format = str(obj.image).split('.')
        obj.image.name = str(obj.name) + '.' + image_format
        return super().save_model(request, obj, form, change)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'pub_date', )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', )
    list_filter = ('ingredient__name', )
