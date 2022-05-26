from django.urls import path
from .views import control, ajax_exec, ajax_copy_to_clipboard, logout

urlpatterns = [
    path('', control, name='control'),

    path('ajax/execute/', ajax_exec, name='ajax-exec-command'),
    path('ajax/copy/', ajax_copy_to_clipboard, name='ajax-copy-to-clipboard'),

    path('logout/', logout, name='logout'),
]
