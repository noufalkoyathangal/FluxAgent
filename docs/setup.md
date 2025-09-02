# Quick Setup Guide

## Prerequisites
1. **Python 3.9+** installed on your system
2. **Azure OpenAI account** with API access
3. **Git** for version control

## Quick Start (5 minutes)

### 1. Clone and Setup
```bash
# Clone the project
git clone <your-repo-url>
cd ai_agent_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Azure OpenAI
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your Azure OpenAI credentials:
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
```

### 3. Run the Application

**Terminal 1 - Start Backend:**
```bash
# Make script executable (Unix/macOS)
chmod +x run_api.sh
./run_api.sh

# Or manually:
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Start Frontend:**
```bash
# Make script executable (Unix/macOS)
chmod +x run_ui.sh
./run_ui.sh

# Or manually:
streamlit run ui/streamlit_app.py --server.port 8501
```

### 4. Access the Application
- **Frontend UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Windows Users

Create these batch files for easy startup:

**run_api.bat:**
```batch
@echo off
call venv\Scripts\activate
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
pause
```

**run_ui.bat:**
```batch
@echo off
call venv\Scripts\activate
streamlit run ui\streamlit_app.py --server.port 8501
pause
```

## Troubleshooting

### Common Issues

1. **"Azure OpenAI API key not found"**
   - Make sure `.env` file exists and contains correct credentials
   - Check that environment variables are set correctly

2. **"Connection refused" or API not available**
   - Ensure FastAPI backend is running on port 8000
   - Check firewall settings
   - Verify no other services are using the ports

3. **"Module not found" errors**
   - Make sure virtual environment is activated
   - Run `pip install -r requirements.txt` again

4. **Streamlit UI can't connect to backend**
   - Start FastAPI backend first (Terminal 1)
   - Then start Streamlit frontend (Terminal 2)
   - Check that both services are running on correct ports

### Getting Azure OpenAI Credentials

1. Go to [Azure Portal](https://portal.azure.com)
2. Create or navigate to your Azure OpenAI resource
3. Go to "Keys and Endpoint" section
4. Copy:
   - **API Key**: One of the available keys
   - **Endpoint**: The endpoint URL
   - **Deployment Name**: Name of your GPT model deployment

### Testing the Setup

1. **Check API Health:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Test Chat Endpoint:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "Hello, how are you?"}'
   ```

3. **Use Example Queries in UI:**
   - "What are the latest trends in AI?"
   - "Research quantum computing developments"
   - "Explain machine learning basics"

## Next Steps

- Explore the **Streamlit UI** at http://localhost:8501
- Check out the **API documentation** at http://localhost:8000/docs
- Try different **agent capabilities** like web search and research
- Customize **agent prompts** in the `app/agents/` directory
- Add **new tools** in the `app/tools/` directory

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review the API docs at `/docs` endpoint
- Create an issue in the repository
- Ensure all environment variables are properly set

---

**You're all set! Start chatting with your AI agent! 🤖**