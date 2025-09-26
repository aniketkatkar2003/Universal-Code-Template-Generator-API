#!/bin/bash

# Universal Code Template Generator API Startup Script

echo "Starting Universal Code Template Generator API..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Start the server
echo "Starting server on http://localhost:8000"
echo "API Documentation available at:"
echo "  - Swagger UI: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"

uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
