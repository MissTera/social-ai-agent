import os
from app.services.conversation_manager import get_conversation_manager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging
from contextlib import asynccontextmanager

from config.settings import settings
from app.models.database import secure_session, Customer, Conversation
from app.utils.security_utils import mask_sensitive_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting {settings.APP_NAME} in {settings.ENVIRONMENT} mode")
    yield
    # Shutdown
    logger.info("Shutting down application")

app = FastAPI(
    title=settings.APP_NAME,
    description="Secure AI Agent for Social Media Customer Service",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = secure_session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}", "status": "healthy"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    # Test database connection
    try:
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy", 
        "service": "social-media-ai-agent",
        "database": db_status
    }

@app.post("/customers/")
async def create_customer(
    email: str,
    social_media_id: str,
    platform: str = "instagram",
    first_name: str = "",
    last_name: str = "",
    db: Session = Depends(get_db)
):
    """Create a new customer record"""
    customer = Customer()
    customer.set_email(email)
    customer.social_media_id = social_media_id
    customer.platform = platform
    customer.first_name = first_name
    customer.last_name = last_name
    
    db.add(customer)
    db.commit()
    db.refresh(customer)
    
    return {
        "id": customer.id,
        "social_media_id": customer.social_media_id,
        "platform": customer.platform,
        "message": "Customer created successfully"
    }

@app.get("/customers/")
async def get_customers(db: Session = Depends(get_db)):
    """Get all customers"""
    customers = db.query(Customer).all()
    return {
        "customers": [
            {
                "id": customer.id,
                "social_media_id": customer.social_media_id,
                "platform": customer.platform,
                "first_name": customer.first_name,
                "created_at": customer.created_at.isoformat()
            } for customer in customers
        ]
    }

@app.post("/ai/chat")
async def ai_chat_endpoint(
    message: str,
    social_media_id: str,
    platform: str = "instagram",
    db: Session = Depends(get_db)
):
    """Main endpoint for AI chat conversations"""
    conversation_manager = get_conversation_manager(db)
    
    result = conversation_manager.process_message(
        user_message=message,
        social_media_id=social_media_id,
        platform=platform
    )
    
    return {
        "success": True,
        "response": result["response"],
        "intent": result["intent"],
        "requires_human": result["requires_human"],
        "customer_id": result["customer_id"],
        "suggested_actions": result["suggested_actions"]
    }

@app.get("/conversations/{customer_id}")
async def get_conversation_history(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """Get conversation history for a customer"""
    conversations = db.query(Conversation).filter(
        Conversation.customer_id == customer_id
    ).order_by(Conversation.created_at.asc()).all()
    
    return {
        "customer_id": customer_id,
        "conversations": [
            {
                "id": conv.id,
                "user_message": conv.message_text,
                "ai_response": conv.ai_response,
                "intent": conv.intent,
                "requires_human": conv.requires_human,
                "timestamp": conv.created_at.isoformat()
            } for conv in conversations
        ]
    }
@app.get("/ai/chat-test")
async def ai_chat_test_endpoint(
    message: str,
    social_media_id: str,
    platform: str = "instagram",
    db: Session = Depends(get_db)
):
    """TEST endpoint for AI chat (GET method for browser testing)"""
    conversation_manager = get_conversation_manager(db)
    
    result = conversation_manager.process_message(
        user_message=message,
        social_media_id=social_media_id,
        platform=platform
    )
    
    return {
        "success": True,
        "response": result["response"],
        "intent": result["intent"],
        "requires_human": result["requires_human"],
        "customer_id": result["customer_id"],
        "suggested_actions": result["suggested_actions"]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    
    )