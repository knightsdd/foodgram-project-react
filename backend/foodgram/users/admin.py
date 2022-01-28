from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Subscription

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'first_name', 'last_name')
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username',)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
