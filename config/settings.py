import os
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    # Application
    APP_NAME: str = "MissTera AI Agent"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Security - These MUST be set in environment variables
    ENCRYPTION_KEY: str
    JWT_SECRET_KEY: str
    
    # AI API
    GROQ_API_KEY: str
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./social_ai_agent.db")
    
    # CORS
    CORS_ORIGINS: list = ["*"]

settings = Settings()