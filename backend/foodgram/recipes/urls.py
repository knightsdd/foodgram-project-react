from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, RecipeListAPIView

recipes_router = DefaultRouter()
recipes_router.register('ingredients', IngredientViewSet)
