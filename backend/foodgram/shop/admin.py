from django.contrib import admin

from .models import ShoppingCart


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipes'
    )
    search_fields = ('user',)


admin.site.register(ShoppingCart, ShoppingCartAdmin)
