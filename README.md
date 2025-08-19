# Adaptive AI Assistant

A sophisticated agentic task management tool that uses dynamic personality profiling to create personalized user experiences. The system features four specialized AI agents working together to provide adaptive responses, intelligent task extraction, and a generative React UI that adapts to user personality traits.

## 🌟 Features

### Core Capabilities
- **Dynamic Personality Profiling**: Builds and maintains persistent user personality profiles using Big Five traits
- **Adaptive Task Extraction**: Extracts and formats tasks based on user personality and preferences
- **Personalized Responses**: Chat responses adapt to user communication style and preferences
- **Generative UI**: React interface that dynamically adapts layout, colors, and interactions based on personality
- **Real-time Communication**: WebSocket support for instant updates and real-time personality adaptation

### AI Agents
1. **Personality Agent**: Analyzes user interactions to build comprehensive personality profiles
2. **Task Agent**: Extracts actionable tasks with personality-driven formatting and prioritization
3. **Chat Agent**: Provides conversational responses adapted to user communication preferences
4. **UI Agent**: Generates adaptive UI configurations based on personality insights

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                         │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │  Chat Interface │ │   Task Panel    │ │Personality Panel││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   FastAPI Backend │
                    │   (WebSocket +    │
                    │   REST API)       │
                    └─────────┬─────────┘
                              │
┌─────────────────────────────┴─────────────────────────────────┐
│                   Agent Manager                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────┐│
│  │ Personality  │ │ Task Agent   │ │ Chat Agent   │ │UI Agent││
│  │ Agent        │ │              │ │              │ │        ││
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   Storage Layer   │
                    │   (SQLite DBs)    │
                    └───────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Environment Setup
1. Clone the repository and navigate to the project directory
2. Create a `.env` file with your API keys:
```bash
PERPLEXITY_API_KEY=your_perplexity_api_key_here
# Optional: Add other provider keys
OPENAI_API_KEY=your_openai_key_here
GROQ_API_KEY=your_groq_key_here
```

### Option 1: Complete System Startup (Recommended)
```bash
python start_system.py
```
This will:
- Install all dependencies (Python + Node.js)
- Start the backend API server
- Start the frontend development server
- Open the application in your browser

### Option 2: Manual Startup

#### Backend Only
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the API server
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Only
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run start
```

#### CLI Interface
```bash
# Run the command-line interface
python main.py
```

## 🎯 Usage

### Web Interface
1. Open your browser to the frontend URL (displayed in startup logs)
2. Start chatting with the AI assistant
3. Watch as the interface adapts to your personality:
   - Colors and themes change based on preferences
   - Layout adjusts to your information density preference
   - Task display formats adapt to your organizational style
   - Response tone matches your communication style

### CLI Interface
1. Run `python main.py`
2. Chat with the assistant
3. Type `profile` to see your current personality analysis
4. Type `exit` to quit

### API Endpoints
- `POST /chat` - Send messages and receive adaptive responses
- `GET /personality-profile` - Get current personality profile
- `POST /ui-config` - Get UI configuration based on personality
- `GET /adaptations` - Get current adaptation suggestions
- `WS /ws` - WebSocket for real-time communication

## 🧠 Personality System

### Traits Analyzed
- **Big Five Personality Traits**:
  - Openness to Experience
  - Conscientiousness
  - Extraversion
  - Agreeableness
  - Neuroticism
- **Communication Style**:
  - Directness
  - Technical Aptitude
  - Formality Preference

### Adaptations
- **Task Agent**: Adjusts task detail level, priority emphasis, and deadline sensitivity
- **Chat Agent**: Modifies response tone, length, formality, and example usage
- **UI Agent**: Changes color schemes, layout density, animation levels, and component arrangements

## 🎨 UI Adaptation Examples

### Personality-Driven Changes
- **High Conscientiousness**: Detailed task views, prominent deadlines, structured layouts
- **High Openness**: Creative color schemes, experimental layouts, rich animations
- **High Extraversion**: Social features emphasized, vibrant colors, dynamic interactions
- **Low Neuroticism**: Calm color palettes, smooth animations, stress-reducing layouts
- **Technical Users**: Dense information display, advanced features visible, minimal explanations

## 📁 Project Structure

```
ai_project/
├── agents/                 # AI agent implementations
│   ├── personality_agent.py   # Dynamic personality profiling
│   ├── task_agent.py          # Adaptive task extraction
│   ├── main_agent.py          # Personalized chat responses
│   ├── ui_agent.py            # Generative UI configuration
│   └── base.py                # Shared agent utilities
├── api/                    # FastAPI backend
│   └── main.py                # REST API and WebSocket endpoints
├── core/                   # Core system components
│   └── agent_manager.py       # Central agent orchestration
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── services/          # API communication
│   │   └── types/             # Type definitions
│   └── package.json
├── storage/                # Data persistence
│   └── loader.py              # Database configuration
├── services/               # Business logic
└── utils/                  # Utility functions
```

## 🔧 Configuration

### Agent Configuration
Modify agent behavior in their respective files:
- `agents/personality_agent.py` - Personality analysis parameters
- `agents/task_agent.py` - Task extraction rules
- `agents/main_agent.py` - Response generation settings
- `agents/ui_agent.py` - UI generation parameters

### UI Themes
The system supports multiple adaptive themes:
- **Light Mode**: Clean, professional appearance
- **Dark Mode**: Reduced eye strain, modern feel
- **Auto Mode**: Adapts based on system preferences
- **Minimal Mode**: Distraction-free, focused interface

### API Providers
Supports multiple AI providers:
- Perplexity (default)
- OpenAI
- Groq

## 🧪 Development

### Adding New Personality Traits
1. Update the personality analysis prompt in `personality_agent.py`
2. Add trait handling in the UI adaptation logic
3. Update the frontend type definitions

### Creating New UI Adaptations
1. Modify the UI agent's generation logic
2. Add corresponding React component adaptations
3. Update the theme system in CSS

### Extending Agent Capabilities
1. Create new agent classes following the existing pattern
2. Register them in the `AgentManager`
3. Add corresponding API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Agno](https://github.com/phidatahq/agno) for AI agent orchestration
- Uses [FastAPI](https://fastapi.tiangolo.com/) for the backend API
- Frontend powered by [React](https://reactjs.org/) and [Tailwind CSS](https://tailwindcss.com/)
- Animations by [Framer Motion](https://www.framer.com/motion/)

## 📞 Support

For questions, issues, or contributions, please open an issue on the GitHub repository.

---

**Adaptive AI Assistant** - Where personality meets technology 🤖✨