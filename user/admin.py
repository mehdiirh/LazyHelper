from django.contrib import admin
from django.contrib.admin import register

from . import models


@register(models.Profile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ['user']
