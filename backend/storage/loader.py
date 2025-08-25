from agno.storage.agent.sqlite import SqliteAgentStorage
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from api.config import settings
import os

Base = declarative_base()
engine = create_async_engine(settings.DATABASE_URL, pool_size=5, max_overflow=10)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def load_session_storage():
    storage_path = os.getenv("AGENT_STORAGE_PATH", "business_agent.db")
    return SqliteAgentStorage(table_name="client_sessions", db_file=storage_path)

def load_personality_storage():
    storage_path = os.getenv("PERSONALITY_STORAGE_PATH", "personality_data.db")
    return SqliteAgentStorage(table_name="personality_sessions", db_file=storage_path)

def load_task_storage():
    storage_path = os.getenv("TASK_STORAGE_PATH", "task_data.db")
    return SqliteAgentStorage(table_name="task_sessions", db_file=storage_path)
