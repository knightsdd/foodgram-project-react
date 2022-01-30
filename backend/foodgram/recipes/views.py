from rest_framework import viewsets, permissions, views, status
from .models import Ingredient, Recipe
from .serializers import (IngredientSerializer, SimpleRecipeSerializer,
                          FavoriteSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


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

    def post(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.user.fav_recipes.filter(recipe_id=recipe_id).exists():
            raise ValidationError(
                detail={'errors': 'Recipe ALREDY in favorite'})
        serializer = FavoriteSerializer(
            data={
                'user': request.user.pk,
                'recipe': recipe_id
                }
            )
        if serializer.is_valid():
            serializer.save(user=request.user, recipe=recipe)
            representation = SimpleRecipeSerializer(recipe)
            return Response(
                representation.data,
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipe_id']
        if not self.request.user.fav_recipes.filter(
                recipe_id=recipe_id).exists():
            raise ValidationError(
                detail={'errors': 'Recipe NOT in favorite'})
        self.request.user.fav_recipes.filter(recipe_id=recipe_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
