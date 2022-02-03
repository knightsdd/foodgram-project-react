from rest_framework.routers import DefaultRouter

from .views import TagViewSet

tag_router = DefaultRouter()
tag_router.register('tags', TagViewSet)
