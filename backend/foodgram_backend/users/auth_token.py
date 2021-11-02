from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import User


class Authenticator(viewsets.ViewSet):

    permission_classes_by_action = {'login': [AllowAny],
                                    'logout': [IsAdminUser | IsAuthenticated]}

    def login(self, request):
        """ Создание токена/аутентификация """
        user = get_object_or_404(
            User, email=request.data.get('email'),
            password=request.data.get('password')
        )
        try:
            token = Token.objects.create(user=user)
        except IntegrityError:
            return Response({'token': str(Token.objects.get(user=user).key)})
        response = {'auth_token': str(token.key)}
        return Response(response, status=status.HTTP_201_CREATED)

    def logout(self, request):
        """ Удаление токена """
        token = Token.objects.get(user=self.request.user)
        token.delete()
        return Response(
            {'status': 'Токен успешно удален'},
            status=status.HTTP_201_CREATED)

    def get_permissions(self):
        try:
            return [permission() for permission
                    in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
