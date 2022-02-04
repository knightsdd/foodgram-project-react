from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteView, IngredientViewSet, RecipeDetailAPIView,
                    RecipeListAPIView)

recipes_router = DefaultRouter()
recipes_router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('', RecipeListAPIView.as_view()),
    path('<int:recipe_id>/', RecipeDetailAPIView.as_view()),
    path('<int:recipe_id>/favorite/', FavoriteView.as_view()),
]
