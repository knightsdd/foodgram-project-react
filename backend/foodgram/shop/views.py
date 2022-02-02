from rest_framework import views, status
from rest_framework.response import Response
from .models import ShoppingCart
from recipes.models import Recipe
from recipes.serializers import SimpleRecipeSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


class ShoppingCartAPIView(views.APIView):

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.user.shopping_cart.filter(recipes=recipe).exists():
            raise ValidationError(
                detail={'errors': 'Recipe ALREDY in shoppingcart'})
        ShoppingCart.objects.create(user=request.user, recipes=recipe)
        serializer = SimpleRecipeSerializer(instance=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if not request.user.shopping_cart.filter(recipes=recipe).exists():
            raise ValidationError(
                detail={'errors': 'Recipe NOT in shoppingcart'})
        ShoppingCart.objects.filter(user=request.user, recipes=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
