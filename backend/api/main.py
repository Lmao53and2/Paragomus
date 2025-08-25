from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from storage.loader import init_db
from api.config import settings
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
import asyncio
from core.agent_manager import AgentManager
from dotenv import load_dotenv
import os



# Load environment variables
load_dotenv()

app = FastAPI(title="Adaptive AI Assistant API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN], # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db()

# Global agent manager instance
agent_manager = None

def get_agent_manager():
    global agent_manager
    if agent_manager is None:
        provider = "Perplexity"
        model = "sonar"
        api_key = os.getenv("PERPLEXITY_API_KEY")
        
        if not api_key:
            raise HTTPException(status_code=500, detail="PERPLEXITY_API_KEY not found")
        
        agent_manager = AgentManager(provider, model, api_key)
    
    return agent_manager

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    context: Optional[str] = ""

class ChatResponse(BaseModel):
    response: str
    personality_profile: Dict[str, Any]
    tasks: Dict[str, Any]
    ui_config: Dict[str, Any]
    adaptations: Dict[str, Any]

class TaskExtraction(BaseModel):
    text: str

class UIConfigRequest(BaseModel):
    context: Optional[str] = ""

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# API Routes
@app.get("/")
async def root():
    return {"message": "Adaptive AI Assistant API", "version": "1.0.0"}

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Main chat endpoint with personality adaptation."""
    try:
        agent = get_agent_manager()
        
        # Generate response
        response = agent.ask(message.message, message.context)
        
        # Extract tasks
        tasks = agent.extract_tasks(message.message)
        
        # Get personality profile
        personality_profile = agent.get_personality_profile()
        
        # Get UI configuration
        ui_config = agent.get_ui_config(message.context)
        
        # Get adaptations
        adaptations = agent.get_adaptation_suggestions()
        
        return ChatResponse(
            response=response,
            personality_profile=personality_profile,
            tasks=tasks,
            ui_config=ui_config,
            adaptations=adaptations
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-tasks")
async def extract_tasks(extraction: TaskExtraction):
    """Extract tasks from text."""
    try:
        agent = get_agent_manager()
        tasks = agent.extract_tasks(extraction.text)
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/personality-profile")
async def get_personality_profile():
    """Get current personality profile."""
    try:
        agent = get_agent_manager()
        return agent.get_personality_profile()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ui-config")
async def get_ui_config(request: UIConfigRequest):
    """Get UI configuration based on personality."""
    try:
        agent = get_agent_manager()
        ui_config = agent.get_ui_config(request.context)
        return ui_config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/adaptations")
async def get_adaptations():
    """Get current adaptation suggestions."""
    try:
        agent = get_agent_manager()
        return agent.get_adaptation_suggestions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/full-context")
async def get_full_context():
    """Get complete context including personality, adaptations, and UI config."""
    try:
        agent = get_agent_manager()
        return agent.get_full_context()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "chat":
                agent = get_agent_manager()
                
                # Process message
                user_message = message_data.get("message", "")
                context = message_data.get("context", "")
                
                # Generate response
                response = agent.ask(user_message, context)
                
                # Get additional data
                tasks = agent.extract_tasks(user_message)
                personality_profile = agent.get_personality_profile()
                ui_config = agent.get_ui_config(context)
                adaptations = agent.get_adaptation_suggestions()
                
                # Send response
                response_data = {
                    "type": "chat_response",
                    "response": response,
                    "personality_profile": personality_profile,
                    "tasks": tasks,
                    "ui_config": ui_config,
                    "adaptations": adaptations
                }
                
                await manager.send_personal_message(json.dumps(response_data), websocket)
            
            elif message_data.get("type") == "ui_update":
                agent = get_agent_manager()
                context = message_data.get("context", "")
                ui_config = agent.get_ui_config(context)
                
                response_data = {
                    "type": "ui_config",
                    "ui_config": ui_config
                }
                
                await manager.send_personal_message(json.dumps(response_data), websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": __import__('time').time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
