from django.contrib import admin
from django.contrib.admin import register

from utils.generators.stylers import render_json
from . import models


@register(models.ReceivedRequest)
class ReceivedRequestsAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'method', 'short_path', 'client_ip', 'status_code', 'status']
    list_display_links = ['id', 'method']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            readonly_fields = ['status', 'path', 'method', 'client_ip', 'pretty_headers',
                               'pretty_data', 'pretty_response',
                               'pretty_private_data', 'status_code', 'message', 'status']
        else:
            readonly_fields = []

        return readonly_fields

    def get_exclude(self, request, obj=None):
        if obj:
            return ['headers', 'sensitive_data', 'response', 'private_data']

    def short_path(self, obj):
        if len(obj.path) > 40:
            return f"{obj.path[:20]} ... {obj.path[-20:]}"
        else:
            return obj.path
    short_path.short_description = 'path'

    def pretty_headers(self, obj):
        return render_json(obj.headers, html=True)
    pretty_headers.short_description = 'Headers'

    def pretty_data(self, obj):
        return render_json(obj.sensitive_data, html=True)
    pretty_data.short_description = 'Data'

    def pretty_response(self, obj):
        return render_json(obj.response, html=True)
    pretty_response.short_description = 'Response'

    def pretty_private_data(self, obj):
        return render_json(obj.private_data, html=True)
    pretty_private_data.short_description = 'Private Data'
