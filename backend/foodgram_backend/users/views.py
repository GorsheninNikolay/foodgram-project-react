from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from .permissions import IsAuthenticatedForDetailOrReadOnly
from .serializers import PasswordSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedForDetailOrReadOnly]

    def get_queryset(self):
        if self.kwargs.get('pk') == 'me':
            self.kwargs['pk'] = self.request.user.id
        return User.objects.all()


class FollowView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | IsAdminUser]
    serializer_class = UserSerializer
    queryset = Follow.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(
            user=self.request.user).values_list(
                'following__username', flat=True
                )
        return User.objects.filter(username__in=queryset)

    def retrieve(self, request, id=None):
        follow = Follow.objects.create(
            user=request.user, following=get_object_or_404(User, id=id)
        )
        user = get_object_or_404(User, id=follow.following.id)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, id=None):
        follow = get_object_or_404(
            Follow, user=request.user,
            following=get_object_or_404(User, id=id))
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
                'new_password'
                )
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
