@echo off
REM ============================================================
REM Quiz Application - One-Step Startup Script (Windows)
REM ============================================================
REM This script automatically:
REM   1. Creates migrations for database schema
REM   2. Applies migrations to SQLite database
REM   3. Creates a default superuser (admin/admin123)
REM   4. Starts the Django development server
REM
REM For questions or issues, check README.md or QUICKSTART.md
REM ============================================================

echo.
echo =====================================================
echo     Quiz Application - Startup Script (Windows)
echo =====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/5] Checking Python installation...
python --version
echo.

REM Check if virtual environment exists, if not create it
if not exist "venv" (
    echo [2/5] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
) else (
    echo [2/5] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated!
echo.

REM Install dependencies
echo [4/5] Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Run migrations
echo [5/5] Setting up database...
echo.
echo   - Creating migrations...
python manage.py makemigrations
if errorlevel 1 (
    echo ERROR: Failed to create migrations
    pause
    exit /b 1
)
echo.

echo   - Applying migrations to database...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to apply migrations
    pause
    exit /b 1
)
echo.

REM Create superuser automatically
echo   - Creating superuser account (admin/admin123)...
python manage.py shell <<PYTHON_END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("   ✓ Superuser 'admin' created with password 'admin123'")
else:
    print("   ✓ Superuser 'admin' already exists")
PYTHON_END
echo.

REM Start development server
echo =====================================================
echo     Database Setup Complete!
echo =====================================================
echo.
echo Starting Django Development Server...
echo.
echo Access the application at:
echo   Home: http://localhost:8000/
echo   Admin: http://localhost:8000/admin/
echo.
echo Admin Credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver
pause
