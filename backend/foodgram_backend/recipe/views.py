from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response

from .models import Favorite, Ingredient, Recipe
from .permissions import IsAuthorOrIsAuthenticatedOrReadOnly
from .serializers import IngredientSerializer


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


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrIsAuthenticatedOrReadOnly]
    serializer_class = 

