from django.urls import include, path
from rest_framework import routers
from users.auth_token import Authenticator

from .views import (FavoriteView, IngredientViewSet, RecipeViewSet,
                    ShoppingCartView, TagViewSet)

router = routers.SimpleRouter()
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path(r'users/', include('users.urls'), name='users'),
    path(r'auth/token/login/', Authenticator.as_view(
        {'post': 'login'}), name='login'),
    path(r'auth/token/logout/', Authenticator.as_view(
        {'post': 'logout'}), name='logout'),
    path(r'ingredients/', IngredientViewSet.as_view({'get': 'list'})),
    path(r'ingredients/<int:id>/', IngredientViewSet.as_view(
        {'get': 'retrieve'})
        ),
    path(r'tags/', TagViewSet.as_view({'get': 'list'})),
    path(r'tags/<int:id>/', TagViewSet.as_view({'get': 'retrieve'})),
    path(r'recipes/<int:id>/favorite/', FavoriteView.as_view()),
    path(r'recipes/<int:id>/shopping_cart/', ShoppingCartView.as_view(
        {'get': 'retrieve', 'delete': 'delete'}
    )),
]

urlpatterns += router.urls
