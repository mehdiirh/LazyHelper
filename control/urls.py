from django.urls import path
from .views import control, logout

urlpatterns = [
    path('', control, name='control'),
    path('logout/', logout, name='logout'),
]
