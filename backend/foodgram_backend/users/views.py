from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Follow, User
from .permissions import IsAuthenticatedForDetailOrReadOnly
from .serializers import (PasswordSerializer, SubscriptionsSerializer,
                          UserSerializer)
from recipes.paginator import BaseLimitPaginator


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedForDetailOrReadOnly]
    pagination_class = BaseLimitPaginator

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
    pagination_class = BaseLimitPaginator
    filter_backends = [DjangoFilterBackend]
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        followings = Follow.objects.filter(
            user=self.request.user).values_list('following', flat=True)
        return queryset.filter(id__in=followings)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = PasswordSerializer
    model = User
    permission_class = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.object.password = serializer.validated_data.get(
            'new_password')
        self.object.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
