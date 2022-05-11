from django.contrib import admin
from django.contrib.admin import register
from django.utils.html import mark_safe

from .models import Config, Command, Button


@register(Config)
class ConfigAdmin(admin.ModelAdmin):

    list_display = ['key', 'active']
    list_editable = ['active']


@register(Command)
class CommandAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'short_code', 'command', 'active']
    list_display_links = ['id', 'title']
    list_editable = ['active']
    prepopulated_fields = {'short_code': ['title']}


@register(Button)
class ButtonAdmin(admin.ModelAdmin):

    list_display = ['command', '_color', 'active']
    list_editable = ['active']

    def _color(self, obj: Button):
        return mark_safe(
            f"""
            <div style="background-color: {obj.color}; height: 100%;">{obj.get_color_display()}</div>
            """
        )
    _color.short_description = 'Color'
    _color.allow_tags = True
