from django.urls import path
from .views import control, ajax_exec, logout

urlpatterns = [
    path('', control, name='control'),

    path('ajax/execute/', ajax_exec, name='ajax-exec-command'),

    path('logout/', logout, name='logout'),
]
