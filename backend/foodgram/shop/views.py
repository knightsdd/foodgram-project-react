import io
import os

from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient, Recipe
from recipes.serializers import SimpleRecipeSerializer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import ShoppingCart


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


class ListForShoppingAPIView(views.APIView):

    def get(self, request):
        user = request.user
        ingredients = (Ingredient.objects
                       .filter(amounts__recipe__customers__user=user)
                       .annotate(amount=Sum('amounts__amount')))

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        font_path = os.path.join(os.path.join(BASE_DIR, 'fonts'), 'Times.ttf')
        pdfmetrics.registerFont(TTFont('Times', font_path))
        p.setFont('Times', 20)
        cursor = 730
        step = 20
        p.setLineWidth(.5)
        p.drawString(230, 770, 'Your shopping list')
        p.setFontSize(size=13)
        for ingredient in ingredients:
            p.drawString(30, cursor, f'- {ingredient} - {ingredient.amount}')
            cursor = cursor - step
        p.line(30, cursor, 560, cursor)
        p.setFontSize(size=10)
        p.drawString(420, cursor - 18, 'Foodgram by KnighT_SD ©')
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename='Your_list.pdf')
