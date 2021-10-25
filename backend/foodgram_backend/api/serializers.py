# from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Follow, Tag


class TagSerializer(ModelSerializer):
    model = Tag
    fields = '__all__'

