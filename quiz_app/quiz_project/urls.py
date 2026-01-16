"""
URL configuration for quiz_project.
"""
from django.urls import path, include

urlpatterns = [
    path('', include('quiz.urls')),
]
