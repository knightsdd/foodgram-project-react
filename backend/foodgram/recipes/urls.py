from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet

recipes_router = DefaultRouter()
recipes_router.register('ingredients', IngredientViewSet)
