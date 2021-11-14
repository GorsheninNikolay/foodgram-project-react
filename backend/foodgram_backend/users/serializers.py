from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Follow, User
from recipes.models import Recipe


class UserSerializer(ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(default=False)

    def get_is_subscribed(self, obj) -> bool:
        user = self.context.get('request').user
        if user is None or not user.is_authenticated:
            return False
        return Follow.objects.filter(user=user, following=obj).exists()

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password', 'is_subscribed'
        )


class ShortRecipeSerializer(ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.IntegerField()

    def get_image(self, obj):
        return obj.image.url

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', )


class SubscriptionsSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit')
        if recipes_limit is not None:
            recipes_limit = int(recipes_limit)
        recipes = Recipe.objects.filter(author=obj)[:recipes_limit]
        return ShortRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        )


class TokenSerializer(ModelSerializer):
    email = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', )


class PasswordSerializer(ModelSerializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['current_password'] != self.context['request'].user.password:
            raise serializers.ValidationError('Неверный пароль.')
        return data

    class Meta:
        model = User
        fields = ('new_password', 'current_password', )
