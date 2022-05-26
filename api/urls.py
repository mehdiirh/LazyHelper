from django.urls import path
from . import views as api_views

urlpatterns = [
    path('execute/', api_views.exec_command, name='exec-command'),
    path('copy/', api_views.copy_to_clipboard, name='copy-to-clipboard'),
    path('commands/', api_views.list_commands, name='list-of-commands'),
]
