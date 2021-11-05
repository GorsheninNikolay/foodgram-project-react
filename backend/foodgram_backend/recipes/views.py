import base64
import os

from django.core.files.base import ContentFile
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .exceptions import UniqueObjectsException
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)
from .pdf_file import create_shopping_cart
from .permissions import IsAuthorOrIsAuthenticatedOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


def get_image(data):
    """ Преобразование кода base64 в картинку ContentFile """
    if (isinstance(data['image'], str)
            and data['image'].startswith('data:image')):
        format, imgstr = data['image'].split(';base64,')
        ext = format.split('/')[-1]
        image = ContentFile(
            base64.b64decode(imgstr), name=data['name'] + '.' + ext
            )
        return image
    return None


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
    parser_classes = (MultiPartParser, JSONParser, )
    filterset_fields = (
        'is_favorited', 'author', 'is_in_shopping_cart', 'tags',
        )

    def create(self, request):
        image = get_image(request.data)
        request.data['image'] = image
        serializer = RecipeSerializer(
            data=request.data, context={'request': request}
            )
        if serializer.is_valid():
            serializer.save(
                author=request.user,
                ingredients=request.data['ingredients'],
                tags=request.data['tags']
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        recipe = Recipe.objects.get(id=pk)
        self.check_object_permissions(request, recipe)
        image = get_image(request.data)
        recipe.image.delete()
        request.data['image'] = image
        serializer = RecipeSerializer(
            recipe, data=request.data, context={'request': request}
            )
        if serializer.is_valid():
            serializer.save(
                ingredients=request.data['ingredients'],
                tags=request.data['tags']
                )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        os.remove(instance.image.path)
        instance.delete()


class FavoriteView(generics.UpdateAPIView):
    model = Favorite
    permission_classes = [IsAdminUser | IsAuthenticated]

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
        data = {}
        shopping_cart = ShoppingCart.objects.filter(author=request.user)
        for shopping in shopping_cart:
            recipe = Recipe.objects.get(id=shopping.recipe.id)
            ingredients = RecipeIngredient.objects.filter(recipe=recipe)
            for recipe_ingredient in ingredients:
                ingredient = recipe_ingredient.ingredient
                if not data.get(ingredient.name):
                    data[ingredient.name] = {
                        'name': ingredient.name,
                        'measurement_unit': ingredient.measurement_unit,
                        'amount': 0
                    }
                data[ingredient.name]['amount'] += recipe_ingredient.amount
        create_shopping_cart(data)
        response = FileResponse(open('media/shopping_cart.pdf', 'rb'))
        return response

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
