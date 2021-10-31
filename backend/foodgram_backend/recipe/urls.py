from django.urls import include, path
from rest_framework import routers
from users.auth_token import Authenticator

from .views import (FavoriteView, IngredientViewSet, RecipeViewSet,
                    ShoppingCartView, TagViewSet)

router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('users/', include('users.urls'), name='users'),
    path('auth/token/login/', Authenticator.as_view(
        {'post': 'login'}), name='login'),
    path('auth/token/logout/', Authenticator.as_view(
        {'post': 'logout'}), name='logout'),
    path('ingredients/', IngredientViewSet.as_view({'get': 'list'})),
    path('ingredients/<int:id>/', IngredientViewSet.as_view(
        {'get': 'retrieve'})
        ),
    path('tags/', TagViewSet.as_view({'get': 'list'})),
    path('tags/<int:id>', TagViewSet.as_view({'get': 'retrieve'})),
    path('recipes/<int:id>/favorite/', FavoriteView.as_view()),
    path('recipes/<int:id>/shopping_cart/', ShoppingCartView.as_view(
        {'get': 'retrieve', 'delete': 'delete'}
    )),
]

urlpatterns += router.urls
