import django_filters
from django.db.models import Q
from users.models import User

from recipes.models import Favorite, Recipe, ShoppingCart


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorited = django_filters.BooleanFilter(
        label='is_favorited', method='is_favorited_filter')
    is_in_shopping_cart = django_filters.BooleanFilter(
        label='is_in_shopping_cart', method='is_in_shopping_cart_filter'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def is_favorited_filter(self, queryset, name, value):
        favorites = Favorite.objects.filter(
            recipe__in=queryset, user=self.request.user).values_list(
                'recipe', flat=True)
        if value is False:
            return queryset.filter(~Q(id__in=favorites))
        return queryset.filter(id__in=favorites)

    def is_in_shopping_cart_filter(self, queryset, name, value):
        shopping_cart = ShoppingCart.objects.filter(
            recipe__in=queryset, user=self.request.user).values_list(
                'recipe', flat=True)
        if value is False:
            return queryset.filter(~Q(id__in=shopping_cart))
        return queryset.filter(id__in=shopping_cart)
