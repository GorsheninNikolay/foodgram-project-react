from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from .serializers import PasswordSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        if (self.kwargs.get('pk') is not None
                and not self.request.user.is_authenticated):
            raise NotAuthenticated()
        if self.kwargs.get('pk') == 'me':
            self.kwargs['pk'] = self.request.user.id
        return User.objects.all()


class FollowView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = Follow.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(
                user=self.request.user
            )
        followings = [user.following for user in queryset]
        queryset = User.objects.filter(username__in=followings)
        return queryset

    def retrieve(self, request, id=None):
        Follow.objects.create(
            user=request.user, following=User.objects.get(id=id)
        )
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, id=None):
        follow = get_object_or_404(
            Follow, user=request.user, following=User.objects.get(id=id)
            )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = PasswordSerializer
    model = User
    permission_class = [IsAuthenticated]

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
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
