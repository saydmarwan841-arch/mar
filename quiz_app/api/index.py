"""
Vercel Serverless Handler for Django
"""
import os
import sys
from pathlib import Path

# Add the project directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')

# Import Django
import django
django.setup()

# Import WSGI application
from quiz_project.wsgi import application

# Create handler for Vercel
def handler(request):
    return application(request)
