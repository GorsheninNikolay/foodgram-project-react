from django.urls import include, path
from rest_framework import routers

from .auth_token import AuthLogin, AuthLogout
from .views import ChangePasswordView, FollowView, GetFollowView, UserViewSet

router = routers.DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('set_password/', ChangePasswordView.as_view()),
    path('subscriptions/', FollowView.as_view({'get': 'list'})),
    path('<int:id>/subscribe/', GetFollowView.as_view()),
]

urlpatterns += router.urls
