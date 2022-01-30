from djoser.views import UserViewSet
from rest_framework.decorators import action
from .serializers import SubscriptionsSerializer
from rest_framework.response import Response
from .models import User
from core.pagination import SubscriptionPagination


class CustomUserViewSet(UserViewSet):

    # TODO: add recipes_limit to pagination

    @action(methods=['get'], detail=False)
    def subscriptions(self, request, *args, **kwargs):
        subs = User.objects.filter(follower__user=request.user)
        self.pagination_class = SubscriptionPagination
        page = self.paginate_queryset(subs)
        if page is not None:
            serializer = SubscriptionsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SubscriptionsSerializer(subs, many=True)
        return Response(serializer.data)
