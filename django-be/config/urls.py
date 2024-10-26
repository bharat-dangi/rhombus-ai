from django.urls import path
from data_processor.views import api

# URL configuration for the Django application
urlpatterns = [
    path('api/', api.urls),  # Root path for API endpoints handled by Django Ninja
]
