from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from .permissions import IsAuthenticatedForDetailOrReadOnly
from .serializers import (PasswordSerializer, SubscriptionsSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedForDetailOrReadOnly]

    def get_queryset(self):
        if self.kwargs.get('pk') == 'me':
            self.kwargs['pk'] = self.request.user.id
        return User.objects.all()

    @action(detail=True,
            methods=['GET', 'DELETE'],
            permission_classes=[IsAuthenticated | IsAdminUser])
    def subscribe(self, request, pk=None):
        if request.method == 'GET':
            follow = Follow.objects.create(
                user=request.user, following=get_object_or_404(User, id=pk))
            user = get_object_or_404(User, id=follow.following.id)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            follow = get_object_or_404(
                Follow, user=request.user,
                following=get_object_or_404(User, id=pk))
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscriptionsViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination

    def list(self, request):
        followings = Follow.objects.filter(
            user=request.user).values_list('following__username', flat=True)
        queryset = self.paginate_queryset(
            User.objects.filter(username__in=followings))
        serializer = SubscriptionsSerializer(
            queryset, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = PasswordSerializer
    model = User
    permission_class = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            self.object.password = serializer.validated_data.get(
                'new_password')
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
