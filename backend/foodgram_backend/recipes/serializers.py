from django.shortcuts import get_object_or_404
from foodgram_backend.settings import MEDIA_URL
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import User
from users.serializers import UserSerializer

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


class RecipeIngredientSerializer(ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    def get_id(self, obj) -> int:
        return obj.ingredient.id

    def get_name(self, obj) -> str:
        return obj.ingredient.name

    def get_measurement_unit(self, obj) -> str:
        return obj.ingredient.measurement_unit

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = RecipeIngredientSerializer(
        source='ingredients_set', many=True
        )
    image = serializers.ImageField(use_url=MEDIA_URL)
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def validate(self, data):
        def validate_fields(self, field, data):
            if self.context['request'].data.get(field) is None:
                raise serializers.ValidationError(
                    {field: 'Обязательное поле.'}
                    )
        validate_fields(self, 'tags', data)
        validate_fields(self, 'image', data)
        validate_fields(self, 'name', data)
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
            author=request.user, recipe=obj
            ).exists()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')
        read_only_fields = ('author', 'tags', )

    def create(self, validated_data):
        validated_data.pop('ingredients_set')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(Tag.objects.filter(
            id__in=tags)
            )
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
                )
        return recipe

    def update(self, instance, validated_data):
        validated_data.pop('ingredients_set')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.name = validated_data['name']
        instance.text = validated_data['text']
        instance.cooking_time = validated_data['cooking_time']
        instance.image = validated_data['image']
        instance.tags.set(
            Tag.objects.filter(
                id__in=tags
                )
            )
        RecipeIngredient.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=instance,
                amount=ingredient['amount']
                )
        instance.save()
        return instance
