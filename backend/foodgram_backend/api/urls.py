from django.urls import include, path
from users.auth_token import AuthLogin, AuthLogout

urlpatterns = [
    path('users/', include('users.urls')),
    path('auth/token/login/', AuthLogin.as_view()),
    path('auth/token/logout/', AuthLogout.as_view()),
]
