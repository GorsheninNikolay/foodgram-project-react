import base64

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator
from users.models import User
from users.serializers import UserSerializer

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(ModelSerializer):
    amount = serializers.SerializerMethodField()

    def get_amount(self, obj) -> int:
        recipeingredint = get_object_or_404(RecipeIngredient, id=obj.id)
        return recipeingredint.amount

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurment_unit', 'amount', )


class FavoriteSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    def get_name(self, obj) -> str:
        return str(obj.recipe.name)

    def get_image(self, obj) -> str:
        return str(obj.recipe.image.url)

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
    ingredients = RecipeIngredientSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    # image = serializers.SerializerMethodField()

    # def get_image(self, obj):
    #     return base64.decodestring(obj.image)

    def get_is_favorited(self, obj) -> bool:
        if not self.context['request'].user.is_authenticated:
            return False
        user = get_object_or_404(User, username=self.context['request'].user)
        favorite = Favorite.objects.filter(user=user, recipe=obj).exists()
        return favorite

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'name', 'image', 'text', 'cooking_time')


class ShoppingCartSerailizer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    def get_name(self, obj) -> str:
        return obj.recipe.name

    def get_image(self, obj) -> str:
        return obj.recipe.image.url

    def get_cooking_time(self, obj) -> str:
        return obj.recipe.cooking_time

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time', )
