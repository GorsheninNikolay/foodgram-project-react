from django.urls import include, path
from rest_framework import routers
from users.auth_token import AuthLogin, AuthLogout

from recipe.views import IngredientViewSet, TagViewSet

from .views import FavoriteView, IngredientViewSet, RecipeViewSet

router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('users/', include('users.urls')),
    path('auth/token/login/', AuthLogin.as_view()),
    path('auth/token/logout/', AuthLogout.as_view()),
    path('ingredients/', IngredientViewSet.as_view({'get': 'list'})),
    path('ingredients/<int:id>/', IngredientViewSet.as_view(
        {'get': 'retrieve'})
        ),
    path('tags/', TagViewSet.as_view({'get': 'list'})),
    path('tags/<int:id>', TagViewSet.as_view({'get': 'retrieve'})),
    path('recipes/<int:id>/favorite/', FavoriteView.as_view()),
]

urlpatterns += router.urls
