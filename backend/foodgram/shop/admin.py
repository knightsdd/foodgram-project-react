from django.contrib import admin
from .models import ShoppingCart


class ShoppingCartAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'recipes'
    )
    list_display = (
        'user',
        'get_recipes',
    )

    def get_recipes(self, obj):
        return ', '.join([r.name for r in obj.recipes.all()])
    get_recipes.short_description = 'Рецепты'


admin.site.register(ShoppingCart, ShoppingCartAdmin)
