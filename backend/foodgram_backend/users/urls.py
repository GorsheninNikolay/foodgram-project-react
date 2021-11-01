from django.urls import path
from rest_framework import routers

from .views import ChangePasswordView, FollowView, UserViewSet

router = routers.DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path(r'set_password/', ChangePasswordView.as_view()),
    path(r'subscriptions/', FollowView.as_view({'get': 'list'})),
    path(r'<int:id>/subscribe/', FollowView.as_view(
        {'get': 'retrieve', 'delete': 'destroy'})),
]

urlpatterns += router.urls
