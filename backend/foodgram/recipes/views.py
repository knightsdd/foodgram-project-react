import base64
import os

from core.pagination import UserPagination
from django.shortcuts import get_object_or_404
from django_filters import CharFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from foodgram.settings import MEDIA_ROOT
from rest_framework import permissions, status, views, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from users.models import User

from .models import Ingredient, Recipe
from .serializers import (AddRecipeSerialier, FavoriteSerializer,
                          FullRecipeSerializer, IngredientSerializer,
                          SimpleRecipeSerializer)


class IngredientFilterSet(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny, ]
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilterSet


class FavoriteView(views.APIView):

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.user.fav_recipes.filter(recipe_id=recipe_id).exists():
            raise ValidationError(
                detail={'errors': 'Recipe ALREDY in favorite'})
        serializer = FavoriteSerializer(
            data={
                'user': request.user.pk,
                'recipe': recipe_id})
        if serializer.is_valid():
            serializer.save(user=request.user, recipe=recipe)
            representation = SimpleRecipeSerializer(recipe)
            return Response(
                representation.data,
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        if not self.request.user.fav_recipes.filter(
                recipe_id=recipe_id).exists():
            raise ValidationError(
                detail={'errors': 'Recipe NOT in favorite'})
        self.request.user.fav_recipes.filter(recipe_id=recipe_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeListAPIView(views.APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        recipes = Recipe.objects.all()
        tags = dict(request.GET).get('tags')
        if tags:
            recipes = recipes.filter(tags__slug__in=tags).distinct()
        if int(request.GET.get('is_favorited', 0)):
            recipes = recipes.filter(fan__user=request.user)
        if int(request.GET.get('is_in_shopping_cart', 0)):
            recipes = recipes.filter(customers__user=request.user)
        if int(request.GET.get('author', 0)):
            author = get_object_or_404(User, pk=request.GET.get('author'))
            recipes = recipes.filter(author=author)
        paginator = UserPagination()
        page = paginator.paginate_queryset(recipes, request)
        if page is not None:
            serializer = FullRecipeSerializer(
                page,
                context={'request': request},
                many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = FullRecipeSerializer(
            recipes,
            context={'request': request},
            many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddRecipeSerialier(
            data=request.data,
            context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetailAPIView(views.APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        serializer = FullRecipeSerializer(
            recipe,
            context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if recipe.author != request.user:
            raise PermissionDenied(
                detail={'detail': 'У вас недостаточно прав для выполнения'
                                  'данного действия.'},
                code=status.HTTP_403_FORBIDDEN)

        file_path = os.path.join(MEDIA_ROOT, str(recipe.image))
        with open(file_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read())
        _, ext = str(recipe.image).split('.')
        if os.path.isfile(file_path):
            os.remove(file_path)
        request.data['image'] = (f'data:/image/{ext};base64,'
                                 f'{encoded_image.decode("utf-8")}')

        serializer = AddRecipeSerialier(
            recipe,
            data=request.data,
            context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if recipe.author != request.user:
            raise PermissionDenied(
                detail={'detail': 'У вас недостаточно прав для выполнения'
                                  'данного действия.'},
                code=status.HTTP_403_FORBIDDEN)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
