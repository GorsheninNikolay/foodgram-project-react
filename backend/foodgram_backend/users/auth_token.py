from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User


class AuthToken(APIView):

    def post(self, request):
        user = get_object_or_404(
            User, email=request.data.get('email'),
            password=request.data.get('password')
        )
        token = Token.objects.create(user=user)
        response = {'token': str(token.key)}
        return Response(response, status=status.HTTP_201_CREATED)
