from django.contrib import admin
from django.contrib.admin import register

from .models import Config


@register(Config)
class ConfigAdmin(admin.ModelAdmin):

    list_editable = ['active']
    list_display = ['key', 'active']
