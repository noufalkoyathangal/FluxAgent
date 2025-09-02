#!/bin/bash

# Script to run the Streamlit UI

echo "🎨 Starting AI Agent Streamlit UI..."
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

# Check if FastAPI backend is running
echo "🔍 Checking if FastAPI backend is running..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "⚠️  FastAPI backend is not running on port 8000."
    echo "   Please start the backend first by running: ./run_api.sh"
    echo "   Or in a separate terminal: uvicorn app.api.main:app --reload"
    echo ""
    echo "   You can still start the UI, but it won't be able to connect to the backend."
    read -p "   Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ FastAPI backend is running"
fi

# Install dependencies if needed
echo "📋 Checking dependencies..."
pip install -q -r requirements.txt

# Start the Streamlit server
echo "🚀 Starting Streamlit UI on http://localhost:8501"
echo "🤖 AI Agent Interface ready!"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="

# Run Streamlit with custom configuration
streamlit run ui/streamlit_app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --browser.gatherUsageStats false \
    --logger.level info