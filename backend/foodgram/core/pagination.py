from rest_framework.pagination import LimitOffsetPagination


class UserPagination(LimitOffsetPagination):
    offset_query_param = 'page'


class SubscriptionPagination(UserPagination):
    pass
