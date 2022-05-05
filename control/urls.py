from django.urls import path
from .views import control

urlpatterns = [
    path('', control, name='control'),
]
