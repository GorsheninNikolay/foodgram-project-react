from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, RecipeIngredient, Tag


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )


admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Favorite)
