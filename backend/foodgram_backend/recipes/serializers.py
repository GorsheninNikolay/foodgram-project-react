import os

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User
from users.serializers import UserSerializer

from .fields import Base64ImageField
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class ShortRecipeSerializer(ModelSerializer):
    id = serializers.IntegerField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    image = serializers.SerializerMethodField()
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    def get_image(self, obj):
        return obj.recipe.image.url

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time', )


class RecipeIngredientSerializer(ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = RecipeIngredientSerializer(
        source='ingredient_set', many=True, read_only=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def validate(self, data):
        ingredients = []
        for ingredient in self.context['request'].data['ingredients']:
            if ingredient in ingredients:
                raise serializers.ValidationError(
                    'Ингредиенты должны быть уникальными.')
            if int(ingredient['amount']) < 0:
                raise serializers.ValidationError(
                    'Обнаружено отрицательное значение.')
            ingredients.append(ingredient)
        return data

    def get_is_favorited(self, obj) -> bool:
        request = self.context['request']
        if request.user is None or not request.user.is_authenticated:
            return False
        user = get_object_or_404(User, username=request.user)
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj) -> bool:
        request = self.context['request']
        if request.user is None or not request.user.is_authenticated:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj).exists()

    def to_representation(self, obj):
        """Отдаю относительную ссылку на картинку,
        чтобы nginx смог поймать ее"""
        result = super().to_representation(obj)
        result['image'] = obj.image.url
        return result

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')
        read_only_fields = ('author', 'tags', )

    def create_or_update_tags_and_ingredients(self, recipe, tags, ingredients):
        recipe.tags.set(Tag.objects.filter(
            id__in=tags))
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient=get_object_or_404(Ingredient, id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount'])

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_or_update_tags_and_ingredients(recipe, tags, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        RecipeIngredient.objects.filter(recipe=instance).delete()
        if self.context['request'].method == 'PUT':
            os.remove(instance.image.path)
        self.create_or_update_tags_and_ingredients(instance, tags, ingredients)
        super().update(instance, validated_data)
        return instance
