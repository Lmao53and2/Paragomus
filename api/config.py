# api/config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PERPLEXITY_API_KEY: str = Field(..., min_length=10)
    OPENAI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    ENV: str = "dev"
    FRONTEND_ORIGIN: str = "http://localhost:5173"
    DATABASE_URL: str = "sqlite+aiosqlite:///./paragomus.db"

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
