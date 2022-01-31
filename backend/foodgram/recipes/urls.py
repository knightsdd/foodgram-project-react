from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, FullRecipeViewSet

recipes_router = DefaultRouter()
recipes_router.register('ingredients', IngredientViewSet)
recipes_router.register('recipes', FullRecipeViewSet)
