from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Favorite, Ingredient, Recipe, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(ModelSerializer):
    ingredients = serializers.SlugRelatedField(
        read_only=True,
        required=False
    )

    def check_is_favorited(self, obj) -> bool:
        if not self.context['request'].user.is_authenticated:
            return False
        user = User.objects.get(username=self.context['request'].user)
        recipe = get_object_or_404(Recipe, )
        is_favorited = Favorite.objects.get(
            recipe = 
            )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited')
