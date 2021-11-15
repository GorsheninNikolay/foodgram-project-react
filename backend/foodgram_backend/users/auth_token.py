from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import TokenSerializer


class Authenticator(viewsets.ViewSet):

    permission_classes_by_action = {'login': [AllowAny],
                                    'logout': [IsAdminUser | IsAuthenticated]}

    def login(self, request):
        """ Создание токена/аутентификация """
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, **request.data)
        token = Token.objects.create(user=user)
        response = {'auth_token': str(token.key)}
        return Response(response, status=status.HTTP_201_CREATED)

    def logout(self, request):
        """ Удаление токена """
        token = get_object_or_404(Token, user=self.request.user)
        token.delete()
        return Response(
            {'status': 'Токен успешно удален'},
            status=status.HTTP_201_CREATED)
