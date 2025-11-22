import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "MissTera AI Agent"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Security - With defaults for development
    ENCRYPTION_KEY: str = "dev-key-not-for-production-12345"
    JWT_SECRET_KEY: str = "dev-jwt-secret-not-for-production-12345"
    
    # AI API - Optional for development
    GROQ_API_KEY: str = "not-set"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./social_ai_agent.db")
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]

    class Config:
        env_file = ".env"

settings = Settings()