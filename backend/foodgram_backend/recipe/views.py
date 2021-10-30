from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .exceptions import UniqueObjectsException
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import IsAuthorOrIsAuthenticatedOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerailizer,
                          TagSerializer)


class IngredientViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Ingredient.objects.all()
        serializer = IngredientSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = Ingredient.objects.all()
        ingredient = get_object_or_404(queryset, pk=id)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)


class TagViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, pk=id)
        serializer = TagSerializer(tag)
        return Response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrIsAuthenticatedOrReadOnly]
    serializer_class = RecipeSerializer


class FavoriteView(generics.UpdateAPIView):
    model = Favorite
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        recipe = Recipe.objects.get(id=id)
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            raise UniqueObjectsException
        favorite = Favorite.objects.create(
            user=request.user, recipe=recipe
        )
        serializer = FavoriteSerializer(favorite)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def delete(self, request, id=None):
        favorite = get_object_or_404(
            Favorite, user=request.user, recipe=Recipe.objects.get(id=id)
            )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, id=None):
        recipe = get_object_or_404(Recipe, id=id)
        if ShoppingCart.objects.filter(
            author=request.user, recipe=recipe).exists():
            raise UniqueObjectsException
        shopping_cart = ShoppingCart.objects.create(
            author=request.user,
            recipe=recipe
        )
        serializer = ShoppingCartSerailizer(shopping_cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id=None):
        shopping_cart = get_object_or_404(
            ShoppingCart, recipe=get_object_or_404(Recipe, id=id)
            )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
