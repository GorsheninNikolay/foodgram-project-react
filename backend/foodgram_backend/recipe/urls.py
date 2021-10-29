from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet

router = routers.DefaultRouter()
router.register()

urlpatterns = [
    path('ingredients/', IngredientViewSet.as_view({'get': 'list'})),
    path('ingredients/<int:id>/', IngredientViewSet.as_view(
        {'get': 'retrieve'})
        ),
]
