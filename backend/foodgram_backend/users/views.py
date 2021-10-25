from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from .serializers import FollowSerializer, PasswordSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_class = IsAuthenticated

    def get_queryset(self):
        if (self.kwargs.get('pk') is not None
                and not self.request.user.is_authenticated):
            raise NotAuthenticated()
        if self.kwargs.get('pk') == 'me':
            self.kwargs['pk'] = self.request.user.id
        return User.objects.all()


class FollowView(viewsets.ModelViewSet):
    model = Follow
    serializer_class = FollowSerializer
    permission_class = IsAuthenticated

    def get_queryset(self):
        return Follow.objects.all()


class GetFollowView(generics.UpdateAPIView):
    model = Follow
    serializer_class = FollowSerializer
    permission_class = IsAuthenticated

    def get(self, request, id=None):
        Follow.objects.create(
            user=request.user, following=User.objects.get(id=id)
        )
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, id=None):
        follow = Follow.objects.get(user=request.user,
                                    following=User.objects.get(id=id))
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = PasswordSerializer
    model = User
    permission_class = IsAuthenticated

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self, request):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if self.object.password != serializer.data.get('current_password'):
                return Response(
                    {'status': 'Неверный пароль'},
                    status=status.HTTP_400_BAD_REQUEST)
            self.object.password = serializer.data.get('new_password')
            self.object.save()
            response = {
                'status': 'Success',
                'code': status.HTTP_200_OK,
                'message': 'Ваш пароль успешно изменен'
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
