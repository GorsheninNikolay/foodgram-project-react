from rest_framework import routers
from django.urls import include, path

from .views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.auth_token import Authenticator

router = routers.SimpleRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path(r'users/', include('users.urls'), name='users'),
    path(r'auth/token/login/', Authenticator.as_view(
        {'post': 'login'}), name='login'),
    path(r'auth/token/logout/', Authenticator.as_view(
        {'post': 'logout'}), name='logout'),
]

urlpatterns += router.urls
