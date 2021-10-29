from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User


class AuthLogin(APIView):
    """ Создание токена/аутентификация """
    def post(self, request):
        user = get_object_or_404(
            User, email=request.data.get('email'),
            password=request.data.get('password')
        )
        token = Token.objects.create(user=user)
        response = {'token': str(token.key)}
        return Response(response, status=status.HTTP_201_CREATED)


class AuthLogout(APIView):
    """ Удаление токена """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = Token.objects.get(user=self.request.user)
        token.delete()
        return Response(
            {'status': 'Токен успешно удален'},
            status=status.HTTP_204_NO_CONTENT)
