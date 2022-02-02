from rest_framework.exceptions import ValidationError
from djoser.views import UserViewSet
from rest_framework.decorators import action
from .serializers import SubscriptionsSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Subscription, User
from django.shortcuts import get_object_or_404


class CustomUserViewSet(UserViewSet):

    @action(methods=['get'], detail=False)
    def subscriptions(self, request, *args, **kwargs):
        subs = User.objects.filter(follower__user=request.user).order_by('-pk')
        page = self.paginate_queryset(subs)
        if page is not None:
            serializer = SubscriptionsSerializer(
                page,
                many=True,
                context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = SubscriptionsSerializer(
            subs,
            many=True,
            context={'request': request})
        # serializer.context = {'request': request}
        return Response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id=None):
        print('AAA ', id)
        author = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            if request.user.following.filter(author=author).exists():
                raise ValidationError(
                    {'errors': 'User ALREDY in subscription'})
            Subscription.objects.create(user=request.user, author=author)
            serializer = SubscriptionsSerializer(
                author,
                context={'request': request})
            return Response(serializer.data)
        else:
            if not request.user.following.filter(author=author).exists():
                raise ValidationError(
                    {'errors': 'User NOT in subscription'})
            Subscription.objects.filter(
                user=request.user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
