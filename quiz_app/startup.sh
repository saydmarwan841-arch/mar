#!/bin/bash

# ============================================================
# Quiz Application - One-Step Startup Script (Linux/Mac)
# ============================================================
# This script automatically:
#   1. Creates migrations for database schema
#   2. Applies migrations to SQLite database
#   3. Creates a default superuser (admin/admin123)
#   4. Starts the Django development server
#
# Usage: chmod +x startup.sh && ./startup.sh
# For questions or issues, check README.md or QUICKSTART.md
# ============================================================

set -e  # Exit on first error

echo ""
echo "====================================================="
echo "    Quiz Application - Startup Script (Unix/Linux)"
echo "====================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python3 from https://www.python.org/downloads/"
    exit 1
fi

echo "[1/5] Checking Python installation..."
python3 --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[2/5] Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created successfully!"
else
    echo "[2/5] Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated!"
echo ""

# Install dependencies
echo "[4/5] Installing dependencies from requirements.txt..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt
echo "Dependencies installed successfully!"
echo ""

# Run migrations
echo "[5/5] Setting up database..."
echo ""
echo "   - Creating migrations..."
python manage.py makemigrations
echo ""

echo "   - Applying migrations to database..."
python manage.py migrate
echo ""

# Create superuser automatically
echo "   - Creating superuser account (admin/admin123)..."
python manage.py shell <<PYTHON_END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("   ✓ Superuser 'admin' created with password 'admin123'")
else:
    print("   ✓ Superuser 'admin' already exists")
PYTHON_END
echo ""

# Start development server
echo "====================================================="
echo "    Database Setup Complete!"
echo "====================================================="
echo ""
echo "Starting Django Development Server..."
echo ""
echo "Access the application at:"
echo "  Home: http://localhost:8000/"
echo "  Admin: http://localhost:8000/admin/"
echo ""
echo "Admin Credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
