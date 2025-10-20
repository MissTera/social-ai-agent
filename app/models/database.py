from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Boolean, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from config.settings import settings
from config.security import encryptor

Base = declarative_base()

class SecureSession:
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

secure_session = SecureSession()

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    email_encrypted = Column(String(255))
    phone_encrypted = Column(String(255))
    social_media_id = Column(String(255), index=True)
    platform = Column(String(50))
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def set_email(self, email: str):
        self.email_encrypted = encryptor.encrypt(email)
    
    def get_email(self) -> str:
        return encryptor.decrypt(self.email_encrypted) if self.email_encrypted else ""

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    platform = Column(String(50))
    message_text = Column(Text)
    ai_response = Column(Text)
    intent = Column(String(100))
    requires_human = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OrderCache(Base):
    __tablename__ = "order_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(100), unique=True, index=True)
    customer_email = Column(String(255))
    order_data = Column(JSON)  # Stores full order details as JSON
    last_updated = Column(DateTime(timezone=True), server_default=func.now())

# Create all tables
Base.metadata.create_all(bind=secure_session.engine)