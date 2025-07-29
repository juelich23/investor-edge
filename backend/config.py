import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Keys
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # CORS
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "https://investor-edge.vercel.app",  # Your production frontend URL
        os.getenv("FRONTEND_URL", "")
    ]
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = ".env"

settings = Settings()