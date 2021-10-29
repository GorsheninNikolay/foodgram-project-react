from django.urls import path
from rest_framework import routers

from .views import ChangePasswordView, FollowView, GetFollowView, UserViewSet

router = routers.DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('set_password/', ChangePasswordView.as_view()),
    path('subscriptions/', FollowView.as_view({'get': 'list'})),
    path('<int:id>/subscribe/', GetFollowView.as_view()),
]

urlpatterns += router.urls
