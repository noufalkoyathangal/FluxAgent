# AI Agent Project

An intelligent AI agent system built with **LangGraph**, **FastAPI**, and **Streamlit**, powered by **Azure OpenAI**. This project demonstrates advanced agentic AI capabilities with a clean, production-ready architecture.

## 🚀 Features

### Core Capabilities
- **Multi-Agent System**: Supervisor and research agents working together
- **Web Search Integration**: Real-time information gathering using DuckDuckGo and Tavily
- **Streaming Responses**: Real-time agent processing feedback
- **Memory Management**: Conversation persistence and context awareness
- **Clean Architecture**: Modular, scalable, and maintainable codebase

### Technical Stack
- **LangGraph**: Orchestrates complex agent workflows
- **Azure OpenAI**: Powers the language model capabilities
- **FastAPI**: High-performance async API backend
- **Streamlit**: Interactive and responsive web interface
- **Pydantic**: Data validation and serialization

## 📁 Project Structure

```
ai_agent_project/
├── app/
│   ├── core/                   # Configuration and core utilities
│   │   ├── config.py          # Application settings
│   │   ├── llm.py             # Azure OpenAI LLM manager
│   │   └── memory.py          # Memory management
│   ├── agents/                # AI agent implementations
│   │   ├── research_agent.py  # Research and information gathering
│   │   ├── supervisor_agent.py # Workflow coordination
│   │   └── base_agent.py      # Base agent class
│   ├── tools/                 # Agent tools and utilities
│   │   ├── web_search.py      # Web search capabilities
│   │   ├── calculator.py      # Mathematical calculations
│   │   └── file_handler.py    # File operations
│   ├── graph/                 # LangGraph workflow definition
│   │   ├── state.py           # Graph state management
│   │   ├── workflow.py        # Main workflow orchestration
│   │   └── nodes.py           # Individual graph nodes
│   ├── api/                   # FastAPI application
│   │   ├── main.py            # FastAPI main app
│   │   ├── routes/            # API endpoints
│   │   └── models/            # Request/response models
│   └── utils/                 # Shared utilities
├── ui/
│   ├── streamlit_app.py       # Main Streamlit interface
│   ├── components/            # UI components
│   └── styles/                # Custom CSS styles
├── tests/                     # Test suite
├── docs/                      # Documentation
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Multi-service orchestration
└── README.md                 # This file
```

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.9+
- Azure OpenAI account and API key
- Git

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd ai_agent_project
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\\Scripts\\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the environment template
cp .env.example .env

# Edit .env with your Azure OpenAI credentials
# Required variables:
# AZURE_OPENAI_API_KEY=your_api_key_here
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
```

### 5. Optional: Install Additional Search Tools
```bash
# For enhanced web search capabilities
pip install duckduckgo-search

# For Tavily search (requires API key)
pip install tavily-python
```

## 🚀 Running the Application

### Method 1: Using Shell Scripts (Recommended)

#### Start the FastAPI Backend
```bash
# Make the script executable (Unix/macOS)
chmod +x run_api.sh
./run_api.sh

# On Windows, create run_api.bat with:
# uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Start the Streamlit Frontend (in a new terminal)
```bash
# Make the script executable (Unix/macOS)
chmod +x run_ui.sh
./run_ui.sh

# On Windows, create run_ui.bat with:
# streamlit run ui/streamlit_app.py --server.port 8501
```

### Method 2: Manual Startup

#### Terminal 1 - FastAPI Backend
```bash
cd ai_agent_project
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 2 - Streamlit Frontend
```bash
cd ai_agent_project
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
streamlit run ui/streamlit_app.py --server.port 8501
```

### Method 3: Docker (Production)
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run separately
docker build -t ai-agent-project .
docker run -p 8000:8000 -p 8501:8501 ai-agent-project
```

## 📖 Usage Guide

### Accessing the Application
1. **FastAPI Backend**: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

2. **Streamlit Frontend**: http://localhost:8501

### Using the Streamlit Interface
1. **Start a Conversation**: Type your message in the chat input
2. **Enable Streaming**: Toggle streaming to see real-time agent processing
3. **Try Example Queries**: Use the provided examples to explore capabilities
4. **Monitor Agent Status**: Watch the sidebar for connection and processing status

### API Endpoints
- `POST /api/v1/chat` - Send a message and get a complete response
- `POST /api/v1/chat/stream` - Stream the agent's processing steps
- `GET /api/v1/chat/history/{conversation_id}` - Retrieve conversation history
- `DELETE /api/v1/chat/{conversation_id}` - Delete a conversation

### Example Queries to Try
- "What are the latest trends in artificial intelligence?"
- "Research quantum computing developments in 2024"
- "Explain machine learning concepts for beginners"
- "Find information about sustainable energy solutions"

## 🔧 Configuration

### Environment Variables
Key configuration options in `.env`:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Application Settings
DEBUG=True
LOG_LEVEL=INFO

# Optional: Enhanced Search APIs
TAVILY_API_KEY=your_tavily_key
SERPAPI_KEY=your_serpapi_key
```

### Agent Configuration
Modify agent behavior in `app/agents/`:
- Adjust prompts and instructions
- Configure tool availability
- Set processing parameters

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_agents.py
pytest tests/test_api.py
pytest tests/test_graph.py

# Run with coverage
pytest --cov=app tests/
```

## 📦 Deployment

### Production Deployment Options

1. **Docker Deployment**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Cloud Platforms**
   - Azure Container Instances
   - AWS ECS/Fargate
   - Google Cloud Run
   - Heroku

3. **Environment Setup**
   - Set production environment variables
   - Configure proper logging levels
   - Enable HTTPS and security headers
   - Set up monitoring and alerting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain Team** for LangGraph framework
- **Microsoft** for Azure OpenAI services
- **FastAPI** and **Streamlit** communities
- **Open source contributors** and maintainers

## 📞 Support

For questions and support:
- Create an issue in the repository
- Check the documentation in the `docs/` folder
- Review the API documentation at `/docs` endpoint

---

**Built with ❤️ using LangGraph, Azure OpenAI, FastAPI, and Streamlit**