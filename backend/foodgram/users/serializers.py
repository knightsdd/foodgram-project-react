from recipes.models import Recipe
from recipes.serializers import SimpleRecipeSerializer
from rest_framework import serializers

from .models import User
from .users_serializers import ShowUserSerializer


class SubscriptionsSerializer(ShowUserSerializer):

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('id', 'is_subscribed', 'recipes_count')

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        limit = int(self.context['request'].GET.get('recipes_limit', 0))
        if limit:
            recipes = obj.recipes.all()[:limit]
        else:
            recipes = obj.recipes.all()
        serializer = SimpleRecipeSerializer(recipes, many=True)
        return serializer.data
