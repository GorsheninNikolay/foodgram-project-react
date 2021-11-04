import base64
import os

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from foodgram_backend.settings import MEDIA_ROOT
from PIL import Image
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .exceptions import UniqueObjectsException
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import IsAuthorOrIsAuthenticatedOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


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
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrIsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = (
        'is_favorited', 'author', 'is_in_shopping_cart', 'tags',
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            image=self.request.data.get('image')
            )

    def perform_destroy(self, instance):
        os.remove(instance.image.path)
        instance.delete()


class FavoriteView(generics.UpdateAPIView):
    model = Favorite
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        recipe = Recipe.objects.get(id=id)
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            raise UniqueObjectsException
        favorite = Favorite.objects.create(
            user=request.user, recipe=recipe
        )
        response = {
            'id': favorite.id,
            'name': favorite.recipe.name,
            'image': (favorite.recipe.image.url
                      if favorite.recipe.image else None),
            'cooking_time': favorite.recipe.cooking_time
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def delete(self, request, id=None):
        favorite = get_object_or_404(
            Favorite, user=request.user, recipe=Recipe.objects.get(id=id)
            )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def download(self, request):
        pass

    def retrieve(self, request, id=None):
        recipe = get_object_or_404(Recipe, id=id)
        if ShoppingCart.objects.filter(
            author=request.user, recipe=recipe
                ).exists():
            raise UniqueObjectsException
        shopping_cart = ShoppingCart.objects.create(
            author=request.user,
            recipe=recipe
        )
        response = {
            'id': shopping_cart.id,
            'name': shopping_cart.recipe.name,
            'image': (shopping_cart.recipe.image.url
                      if shopping_cart.recipe.image else None),
            'cooking_time': shopping_cart.recipe.cooking_time
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def delete(self, request, id=None):
        shopping_cart = get_object_or_404(
            ShoppingCart, recipe=get_object_or_404(Recipe, id=id)
            )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)