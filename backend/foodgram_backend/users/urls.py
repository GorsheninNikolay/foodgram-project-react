from rest_framework import routers

from django.urls import path

from .views import ChangePasswordView, SubscriptionsViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path(r'set_password/', ChangePasswordView.as_view()),
    path(r'subscriptions/', SubscriptionsViewSet.as_view({'get': 'list'}))
]

urlpatterns += router.urls
