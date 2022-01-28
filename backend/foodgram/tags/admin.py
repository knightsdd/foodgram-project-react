from django.contrib import admin
from django.utils.html import format_html
from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'get_color',
        'slug',
    )

    def get_color(self, obj):
        return format_html(
            f'<span style="color: {obj.color};">{obj.color}</span>'
        )
    get_color.short_description = 'Цвет'


admin.site.register(Tag, TagAdmin)
