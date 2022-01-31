from rest_framework import serializers
from .models import Favorite, Ingredient, Recipe, IngredientForRecipe
from tags.serializers import TagSerializer
from users.users_serializers import ShowUserSerializer


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class SimpleRecipeSerializer(serializers.RelatedField):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)

    def get_queryset(self):
        limit = self.context['request'].GET.get('recipes_limit', 0)
        user = self.context['request'].user
        if limit > 0:
            return Recipe.objects.filter(author=user)[:limit]
        return Recipe.objects.filter(author=user)

    def to_representation(self, value):
        data = {
            'id': value.id,
            'name': value.name,
            'image': str(value.image),
            'cooking_time': value.cooking_time
        }
        return data


class FavoriteSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField()
    recipe = serializers.ReadOnlyField()

    class Meta:
        model = Favorite
        fields = '__all__'


class IngredientForRecipeSerializer(serializers.ModelSerializer):

    # amount = serializers.SerializerMethodField()

    class Meta:
        model = IngredientForRecipe
        fields = ('id',)

    def get_amount(self, obj):
        print('AAA', obj)
        return 0


class FullRecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    author = ShowUserSerializer()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return obj.fan.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        return False

    def get_ingredients(self, obj):
        ings = obj.ings_for_recipe.all()
        data = []
        for i in ings:
            data.append(
                {
                    'id': i.ingredient.id,
                    'name': i.ingredient.name,
                    'measurement_unit': i.ingredient.measurement_unit,
                    'amount': i.amount
                }
            )
        return data
