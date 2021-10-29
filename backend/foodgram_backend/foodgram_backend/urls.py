from django.contrib import admin
from django.urls import include, path
from users.auth_token import AuthLogin, AuthLogout

from .views import IngredientViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/auth/token/login/', AuthLogin.as_view()),
    path('api/auth/token/logout/', AuthLogout.as_view()),
    path('api/ingredients/', IngredientViewSet.as_view({'get': 'list'})),
    path('api/ingredients/<int:id>/', IngredientViewSet.as_view(
        {'get': 'retrieve'})
        ),
    path('api/recipes/', include('recipe.urls'))
]
