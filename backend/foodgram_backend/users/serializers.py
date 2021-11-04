from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Follow, User


class UserSerializer(ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(default=False)

    def get_is_subscribed(self, obj) -> bool:
        user = obj
        if user is None or not user.is_authenticated:
            return False
        user = User.objects.get(username=obj)
        following = User.objects.get(username=obj.username)
        follow = Follow.objects.filter(user=user, following=following).exists()
        return follow

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password', 'is_subscribed'
        )


class PasswordSerializer(ModelSerializer):
    model = User
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('new_password', 'current_password',)
