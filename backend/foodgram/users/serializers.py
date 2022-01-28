from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer

from .models import User

# import re


class ShowUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed',)
        read_only_fields = ('id', 'is_subscribed',)

    def get_is_subscribed(self, obj):
        return False


class AfterCreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',)


class CreateUserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password',)
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True, 'write_only': True},
            }

    # def validate_username(self, value):
      #  if not re.match(r'[\w.@+-]+\z', value):
       #     raise serializers.ValidationError("Invalid username")
        # return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email already exists"
            )
        return value

    def to_representation(self, instance):
        s = AfterCreateUserSerializer()
        return s.to_representation(instance=instance)
