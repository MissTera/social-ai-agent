import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Application
    APP_NAME = os.getenv("APP_NAME", "Social Media AI Agent")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # Security
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./social_ai_agent.db")
    
    # CORS
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]

settings = Settings()