from django.contrib import admin

from .models import IngredientForRecipe, Ingredient, Recipe, Favorite


class IngredientForRecipeInline(admin.TabularInline):
    model = IngredientForRecipe
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientForRecipeInline,)
    fields = (
        'author',
        'name',
        'count_favorite',
        'text',
        'image',
        'tags',
        'cooking_time',
    )
    list_display = (
        'author',
        'name',
        'count_favorite',
    )
    search_fields = ('name',)
    list_filter = ('author', 'tags',)
    readonly_fields = ('count_favorite',)

    def count_favorite(self, obj):
        return obj.fan.all().count()
    count_favorite.short_description = 'В избранном'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
