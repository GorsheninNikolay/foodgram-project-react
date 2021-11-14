from django.urls import path

from rest_framework import routers

from .views import ChangePasswordView, SubscriptionsViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path(r'set_password/', ChangePasswordView.as_view()),
    path(r'subscriptions/', SubscriptionsViewSet.as_view({'get': 'list'}))
]

urlpatterns += router.urls
