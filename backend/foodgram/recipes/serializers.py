from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from tags.models import Tag
from tags.serializers import TagSerializer
from users.users_serializers import ShowUserSerializer

from .models import Favorite, Ingredient, IngredientForRecipe, Recipe


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class SimpleRecipeSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)

    def get_image(self, obj):
        return obj.image.url


class FavoriteSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField()
    recipe = serializers.ReadOnlyField()

    class Meta:
        model = Favorite
        fields = '__all__'


class FullRecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    author = ShowUserSerializer()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.fan.filter(user=user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.customers.filter(user=user).exists()
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

    def get_image(self, obj):
        return obj.image.url


class IngredientForRecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class AddRecipeSerialier(serializers.ModelSerializer):

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True,)
    ingredients = IngredientForRecipeSerializer(many=True, required=True)
    image = Base64ImageField()
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'pub_date',
            'author')
        read_only_fields = ('pub_date', 'author')

    def validate_cooking_time(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                {'error': 'Время приготовления не может быть '
                 'нулевым или отрицательным числом'})
        return value

    def validate_ingredients(self, value):
        for i in value:
            if i['amount'] <= 0:
                raise serializers.ValidationError(
                    {'error': 'Количество не может быть '
                     'нулевым или отрицательным числом'})
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        for i in ingredients:
            ingredient = get_object_or_404(Ingredient, pk=i.get('id'))
            IngredientForRecipe.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                amount=i.get('amount'))
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.image = validated_data.get('image')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.tags.clear()
        for tag in validated_data.get('tags'):
            instance.tags.add(tag)
        instance.ings_for_recipe.all().delete()
        for i in validated_data.get('ingredients'):
            ingredient = get_object_or_404(Ingredient, pk=i.get('id'))
            IngredientForRecipe.objects.create(
                ingredient=ingredient,
                recipe=instance,
                amount=i.get('amount')
            )
        instance.save()
        return instance

    def to_representation(self, instance):
        s = FullRecipeSerializer(context=self.context)
        return s.to_representation(instance=instance)
