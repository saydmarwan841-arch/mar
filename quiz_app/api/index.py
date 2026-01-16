"""
Vercel Serverless Handler for Django
"""
import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_dir = str(Path(__file__).resolve().parent.parent)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')

# Configure Django
import django
from django.conf import settings

if not settings.configured:
    django.setup()

# Import WSGI application
from django.core.wsgi import get_wsgi_application

wsgi_app = get_wsgi_application()

# Handler for Vercel
def handler(event, context):
    """
    Main handler for Vercel serverless function
    """
    # Create a mock WSGI environ from the event
    environ = {
        'REQUEST_METHOD': event.get('httpMethod', 'GET'),
        'SCRIPT_NAME': '',
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': event.get('queryStringParameters', ''),
        'CONTENT_TYPE': event.get('headers', {}).get('content-type', ''),
        'CONTENT_LENGTH': event.get('headers', {}).get('content-length', ''),
        'SERVER_NAME': event.get('headers', {}).get('host', 'localhost'),
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': None,
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': True,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    # Add headers to environ
    headers = event.get('headers', {})
    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = f'HTTP_{key}'
        environ[key] = value
    
    # Call WSGI application
    response_started = False
    status = None
    response_headers = None
    
    def start_response(status_str, headers):
        nonlocal response_started, status, response_headers
        response_started = True
        status = int(status_str.split()[0])
        response_headers = dict(headers)
        return lambda s: None
    
    try:
        response = wsgi_app(environ, start_response)
        body = b''.join(response)
        
        return {
            'statusCode': status or 200,
            'headers': response_headers or {},
            'body': body.decode('utf-8') if isinstance(body, bytes) else str(body),
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Internal Server Error: {str(e)}',
        }

