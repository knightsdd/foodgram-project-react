from django.urls import path

from .views import ListForShoppingAPIView, ShoppingCartAPIView

urlpatterns = [
    path('<int:recipe_id>/shopping_cart/', ShoppingCartAPIView.as_view()),
    path('download_shopping_cart/', ListForShoppingAPIView.as_view()),
]
