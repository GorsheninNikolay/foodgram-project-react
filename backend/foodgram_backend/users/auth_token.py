from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import TokenSerializer


class Authenticator(viewsets.ViewSet):

    permission_classes_by_action = {'login': [AllowAny],
                                    'logout': [IsAdminUser | IsAuthenticated]}

    def login(self, request):
        """ Создание токена/аутентификация """
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, **request.data
            )
            token = Token.objects.create(user=user)
            response = {'auth_token': str(token.key)}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def logout(self, request):
        """ Удаление токена """
        token = get_object_or_404(Token, user=self.request.user)
        token.delete()
        return Response(
            {'status': 'Токен успешно удален'},
            status=status.HTTP_201_CREATED)
