import logging
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.database import Conversation, Customer
from app.services.ai_service import ai_service

logger = logging.getLogger(__name__)

class ConversationManager:
    def __init__(self, db: Session):
        self.db = db
    
    def process_message(self, user_message: str, social_media_id: str, platform: str = "instagram") -> Dict[str, Any]:
        """Process incoming message and generate AI response"""
        
        # Find or create customer
        customer = self._get_or_create_customer(social_media_id, platform)
        
        # Get conversation history
        conversation_history = self._get_conversation_history(customer.id)
        
        # Get customer context (will be enhanced with POS data later)
        customer_context = self._get_customer_context(customer)
        
        # Generate AI response
        ai_result = ai_service.generate_response(
            user_message=user_message,
            customer_context=customer_context,
            conversation_history=conversation_history
        )
        
        # Save conversation to database
        self._save_conversation(
            customer_id=customer.id,
            platform=platform,
            user_message=user_message,
            ai_response=ai_result["response"],
            intent=ai_result["intent"],
            requires_human=ai_result["requires_human"]
        )
        
        return {
            "response": ai_result["response"],
            "intent": ai_result["intent"],
            "requires_human": ai_result["requires_human"],
            "customer_id": customer.id,
            "suggested_actions": self._get_suggested_actions(ai_result["intent"])
        }
    
    def _get_or_create_customer(self, social_media_id: str, platform: str) -> Customer:
        """Find existing customer or create new one"""
        customer = self.db.query(Customer).filter(
            Customer.social_media_id == social_media_id,
            Customer.platform == platform
        ).first()
        
        if not customer:
            customer = Customer()
            customer.social_media_id = social_media_id
            customer.platform = platform
            customer.first_name = "Social"
            customer.last_name = "User"
            
            self.db.add(customer)
            self.db.commit()
            self.db.refresh(customer)
            logger.info(f"Created new customer: {customer.id}")
        
        return customer
    
    def _get_conversation_history(self, customer_id: int) -> List[Dict]:
        """Get recent conversation history for context"""
        conversations = self.db.query(Conversation).filter(
            Conversation.customer_id == customer_id
        ).order_by(Conversation.created_at.desc()).limit(10).all()
        
        history = []
        for conv in reversed(conversations):  # Oldest first
            history.append({"role": "user", "content": conv.message_text})
            history.append({"role": "assistant", "content": conv.ai_response})
        
        return history
    
    def _get_customer_context(self, customer: Customer) -> Dict[str, Any]:
        """Get customer context for AI (will be enhanced with POS data later)"""
        return {
            "customer_name": f"{customer.first_name} {customer.last_name}".strip(),
            "customer_email": customer.get_email(),
            "recent_orders": [],  # Will be populated from POS later
            "conversation_count": self.db.query(Conversation).filter(
                Conversation.customer_id == customer.id
            ).count()
        }
    
    def _save_conversation(self, customer_id: int, platform: str, user_message: str, 
                          ai_response: str, intent: str, requires_human: bool):
        """Save conversation to database"""
        conversation = Conversation(
            customer_id=customer_id,
            platform=platform,
            message_text=user_message,
            ai_response=ai_response,
            intent=intent,
            requires_human=requires_human
        )
        
        self.db.add(conversation)
        self.db.commit()
        logger.info(f"Saved conversation for customer {customer_id}, intent: {intent}")
    
    def _get_suggested_actions(self, intent: str) -> List[str]:
        """Get suggested next actions based on intent"""
        actions = {
            'order_status': ["Ask for order number", "Check email for order confirmation", "Provide tracking information"],
            'product_info': ["Share product link", "Check inventory", "Suggest similar products"],
            'shipping': ["Provide shipping timeline", "Check carrier information", "Update delivery status"],
            'returns': ["Escalate to returns specialist", "Provide return instructions", "Process refund"],
            'general_help': ["Offer assistance", "Provide contact information", "Suggest help resources"]
        }
        
        return actions.get(intent, ["Continue conversation"])

# Global conversation manager (will be initialized with database session)
def get_conversation_manager(db: Session):
    return ConversationManager(db)