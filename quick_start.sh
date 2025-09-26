#!/bin/bash

# 🎯 INTERVIEW QUICK START SCRIPT
# Universal Code Template Generator API

echo "🎯 UNIVERSAL CODE TEMPLATE GENERATOR API"
echo "🎪 Interview Demonstration Setup"
echo "================================================="

# Check if we're in the right directory
if [ ! -f "src/main.py" ]; then
    echo "❌ Error: Please run this from the Universal_code_template directory"
    exit 1
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "   Please create it first: python3 -m venv venv"
    exit 1
fi

echo "✅ Project directory confirmed"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "📦 Checking dependencies..."
python -c "import fastapi, uvicorn, pydantic, pytest, requests, httpx" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing missing dependencies..."
    pip install -r requirements.txt
fi

echo "✅ Dependencies ready"

# Run tests to verify everything works
echo "🧪 Running quick test verification..."
python -c "
import sys
sys.path.append('.')
from src.service import TemplateService
from src.models import *

# Quick test
service = TemplateService()
request = TemplateRequest(
    question_id='test',
    title='Test',
    description='Test',
    signature=FunctionSignature(
        function_name='test',
        parameters=[Parameter(name='x', type='int')],
        returns=ReturnType(type='int')
    ),
    language='python'
)
result = service.generate_template(request)
print('✅ Core functionality verified')
"

if [ $? -ne 0 ]; then
    echo "❌ Core functionality test failed"
    exit 1
fi

echo "✅ System verification complete"
echo ""
echo "🚀 READY FOR INTERVIEW DEMO!"
echo "================================================="
echo ""
echo "📋 DEMO OPTIONS:"
echo ""
echo "1️⃣  LIVE API DEMO (Recommended):"
echo "   Terminal 1: ./quick_start.sh server"
echo "   Terminal 2: ./quick_start.sh demo"
echo ""
echo "2️⃣  OFFLINE DEMO (Backup):"
echo "   ./quick_start.sh offline"
echo ""
echo "3️⃣  RUN TESTS:"
echo "   ./quick_start.sh test"
echo ""
echo "4️⃣  MANUAL SERVER:"
echo "   uvicorn src.main:app --host 127.0.0.1 --port 8000"
echo ""

# Handle command line arguments
case "$1" in
    "server")
        echo "🚀 Starting API server for interview demo..."
        echo "📖 Interactive docs will be available at: http://127.0.0.1:8000/docs"
        echo "🔄 Press Ctrl+C to stop server"
        echo ""
        uvicorn src.main:app --host 127.0.0.1 --port 8000
        ;;
    
    "demo")
        echo "🎬 Starting LIVE interview demonstration..."
        echo "💡 Make sure server is running in another terminal!"
        sleep 2
        python interview_demo.py
        ;;
    
    "offline")
        echo "🎬 Starting OFFLINE demonstration..."
        python demo.py
        ;;
    
    "test")
        echo "🧪 Running comprehensive test suite..."
        pytest tests/ -v --no-cov
        ;;
    
    *)
        echo "💡 Use one of the commands above to start your demo!"
        echo ""
        echo "🎯 FOR INTERVIEW: Run these in 2 terminals:"
        echo "   Terminal 1: ./quick_start.sh server"
        echo "   Terminal 2: ./quick_start.sh demo"
        ;;
esac
