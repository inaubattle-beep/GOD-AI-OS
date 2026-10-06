from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "god-ai-os-dev-secret-key-32-chars-long-minimum-key!"
    
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000"]
    
    DATABASE_URL: str = "sqlite+aiosqlite:///./god_ai_os.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    VECTOR_STORE_PROVIDER: str = "sqlite"
    MCP_SERVER_TIMEOUT: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
