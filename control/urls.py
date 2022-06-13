from django.urls import path
from . import views

urlpatterns = [
    path('', views.control, name='control'),

    path('ajax/initial/', views.initial_data, name='ajax-initial-data'),
    path('ajax/execute/', views.ajax_exec, name='ajax-exec-command'),
    path('ajax/copy/', views.ajax_copy_to_clipboard, name='ajax-copy-to-clipboard'),
    path('ajax/login/', views.login, name='ajax-login'),

    path('logout/', views.logout, name='logout'),
]
