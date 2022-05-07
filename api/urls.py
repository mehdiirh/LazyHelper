from django.urls import path
from . import views as api_views

urlpatterns = [
    path('execute/', api_views.exec_command, name='exec-command'),
]
