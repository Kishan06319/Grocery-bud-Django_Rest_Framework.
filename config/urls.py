"""
URL configuration for drf_crud project.
"""
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/health/', views.health, name='health'),
    path('api/grocery/', include('grocery.urls')),
]