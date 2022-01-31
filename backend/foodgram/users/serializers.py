from rest_framework import serializers

from .models import User
from recipes.models import Recipe
from recipes.serializers import SimpleRecipeSerializer
from .users_serializers import ShowUserSerializer


class SubscriptionsSerializer(ShowUserSerializer):

    recipes = SimpleRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('id', 'is_subscribed', 'recipes_count')

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
