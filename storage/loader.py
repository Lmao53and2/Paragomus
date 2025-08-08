from agno.storage.agent.sqlite import SqliteAgentStorage
import os

def load_session_storage():
    storage_path = os.getenv("AGENT_STORAGE_PATH", "business_agent.db")
    return SqliteAgentStorage(table_name="client_sessions", db_file=storage_path)

def load_personality_storage():
    storage_path = os.getenv("PERSONALITY_STORAGE_PATH", "personality_data.db")
    return SqliteAgentStorage(table_name="personality_sessions", db_file=storage_path)

def load_task_storage():
    storage_path = os.getenv("TASK_STORAGE_PATH", "task_data.db")
    return SqliteAgentStorage(table_name="task_sessions", db_file=storage_path)
