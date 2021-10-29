from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from .models import Favorite, Ingredient, Recipe, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class FavoriteSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    def get_name(self, obj) -> str:
        return str(obj.recipe.name)

    def get_image(self, obj) -> str:
        return str(obj.recipe.image)

    def get_cooking_time(self, obj) -> str:
        return str(obj.recipe.cooking_time)

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['recipe', 'user']
            )
        ]


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)

    # def get_is_favorited(self, obj) -> bool:
    #     return True
    #     if not self.context['request'].user.is_authenticated:
    #         return False
    #     user = User.objects.get(username=self.context['request'].user)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')
