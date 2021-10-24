from django.urls import include, path
from rest_framework import routers
from users.auth_token import AuthToken
from users.views import ChangePasswordView, UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('users/set_password/', ChangePasswordView.as_view()),
    path('auth/token/login/', AuthToken.as_view())
]

urlpatterns += router.urls
