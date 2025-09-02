#!/bin/bash

# Script to run the FastAPI backend server

echo "🚀 Starting AI Agent FastAPI Backend..."
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run:"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Please copy .env.example to .env and configure your settings."
    echo "   cp .env.example .env"
    echo ""
    echo "Required environment variables:"
    echo "   - AZURE_OPENAI_API_KEY"
    echo "   - AZURE_OPENAI_ENDPOINT"
    echo "   - AZURE_OPENAI_DEPLOYMENT_NAME"
    exit 1
fi

# Install dependencies if needed
echo "📋 Checking dependencies..."
pip install -q -r requirements.txt

# Start the FastAPI server
echo "🔥 Starting FastAPI server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "💓 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="

# Run the server with auto-reload for development
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload --log-level info