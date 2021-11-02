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
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurment_unit', )


class RecipeIngredientSerializer(ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurment_unit = serializers.SerializerMethodField()

    def get_id(self, obj) -> int:
        return obj.ingredient.id

    def get_name(self, obj) -> str:
        return obj.ingredient.name

    def get_measurment_unit(self, obj) -> str:
        return obj.ingredient.measurment_unit

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurment_unit', 'amount', )


class FavoriteSerializer(ModelSerializer):
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
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['recipe', 'user']
            )
        ]


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = RecipeIngredientSerializer(
        source='ingredients_set', many=True
        )
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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
            author=request.user, recipe=obj
            ).exists()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')
        read_only_fields = ('author', 'image', 'tags', )

    def create(self, validated_data):
        validated_data.pop('ingredients_set')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(Tag.objects.filter(
            id__in=self.context['request'].data['tags'])
            )
        for ingredient in self.context['request'].data['ingredients']:
            RecipeIngredient.objects.create(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
                )
        return recipe

    def update(self, instance, validated_data):
        validated_data.pop('ingredients_set')
        RecipeIngredient.objects.filter(recipe=instance).delete()
        instance.name = validated_data['name']
        instance.text = validated_data['text']
        instance.cooking_time = validated_data['cooking_time']
        instance.tags.set(
            Tag.objects.filter(
                id__in=self.context['request'].data['tags']
                )
            )
        for ingredient in self.context['request'].data['ingredients']:
            RecipeIngredient.objects.create(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=instance,
                amount=ingredient['amount']
                )
        instance.save()
        return instance


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
