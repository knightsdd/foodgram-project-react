from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet


user_router = DefaultRouter()
user_router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    # add paths of djoser
    path('', include(user_router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
