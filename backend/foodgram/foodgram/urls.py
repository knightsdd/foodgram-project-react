from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
)
from tags.urls import tag_router
from recipes.urls import recipes_router
from recipes.views import RecipeListAPIView, RecipeDetailAPIView, FavoriteView
from shop.views import ShoppingCartAPIView, ListForShoppingAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(tag_router.urls)),
    path('api/', include(recipes_router.urls)),
    path('api/', include('users.urls')),
    path('api/recipes/', RecipeListAPIView.as_view()),
    path('api/recipes/<int:recipe_id>/', RecipeDetailAPIView.as_view()),
    path(
        'api/recipes/<int:recipe_id>/shopping_cart/',
        ShoppingCartAPIView.as_view()),
    path(
        'api/recipes/download_shopping_cart/',
        ListForShoppingAPIView.as_view()),
    path(
        'api/recipes/<int:recipe_id>/favorite/',
        FavoriteView.as_view()),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'),
    path(
        'api/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'),
]
