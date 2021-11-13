import os

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .exceptions import UniqueObjectsException
from .filters import IngredientFilter, RecipeFilter
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)
from .paginator import BaseLimitPaginator
from .pdf_file import create_shopping_cart
from .permissions import IsAuthorOrIsAuthenticatedOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShortRecipeSerializer, TagSerializer)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = BaseLimitPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = [IsAuthorOrIsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, JSONParser, )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            tags=self.request.data['tags'],
            ingredients=self.request.data['ingredients']
        )

    def perform_update(self, serializer):
        serializer.save(
            author=self.request.user,
            tags=self.request.data['tags'],
            ingredients=self.request.data['ingredients']
        )

    def perform_destroy(self, instance):
        os.remove(instance.image.path)
        instance.delete()

    @action(detail=True,
            methods=['GET', 'DELETE'],
            permission_classes=[IsAuthenticated | IsAdminUser])
    def favorite(self, request, pk=None):
        if request.method == 'GET':
            recipe = get_object_or_404(Recipe, id=pk)
            if Favorite.objects.filter(
                user=request.user,
                    recipe=recipe).exists():
                raise UniqueObjectsException
            favorite = Favorite.objects.create(
                user=request.user, recipe=recipe)
            serializer = ShortRecipeSerializer(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            favorite = get_object_or_404(
                Favorite, user=request.user, recipe=Recipe.objects.get(id=pk))
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=['GET'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        data = {}
        shopping_cart = ShoppingCart.objects.filter(
            user=request.user).values_list('recipe', flat=True)
        ingredients = RecipeIngredient.objects.filter(recipe__in=shopping_cart)
        for recipe_ingredient in ingredients:
            ingredient = recipe_ingredient.ingredient
            if not data.get(ingredient.name):
                data[ingredient.name] = {
                    'name': ingredient.name,
                    'measurement_unit': ingredient.measurement_unit,
                    'amount': 0
                }
            data[ingredient.name]['amount'] += recipe_ingredient.amount
        return create_shopping_cart(data)

    @action(detail=True,
            methods=['GET', 'DELETE'],
            permission_classes=[IsAuthenticated | IsAdminUser])
    def shopping_cart(self, request, pk=None):
        if request.method == 'GET':
            recipe = get_object_or_404(Recipe, id=pk)
            if ShoppingCart.objects.filter(
                user=request.user,
                    recipe=recipe).exists():
                raise UniqueObjectsException
            shopping_cart = ShoppingCart.objects.create(
                user=request.user,
                recipe=recipe)
            serializer = ShortRecipeSerializer(shopping_cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            shopping_cart = get_object_or_404(
                ShoppingCart, recipe=get_object_or_404(Recipe, id=pk))
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)
