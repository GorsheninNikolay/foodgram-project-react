from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow, User


class UserSerializer(ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(default=False)

    def get_is_subscribed(self, obj) -> bool:
        if not self.context['request'].user.is_authenticated:
            return False
        user = User.objects.get(username=self.context['request'].user)
        following = User.objects.get(username=obj)
        follow = Follow.objects.filter(user=user, following=following).exists()
        return follow

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password', 'is_subscribed'
        )


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        many=False,
        required=False,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        required=True
    )

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя'
            )
        return data

    class Meta:
        model = Follow
        fields = ['user', 'following']

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]


class PasswordSerializer(ModelSerializer):
    model = User
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('new_password', 'current_password',)
