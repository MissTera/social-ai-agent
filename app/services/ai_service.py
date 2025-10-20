import os
import logging
from typing import Dict, Any, List
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1"
        self.conversation_history = {}
    
    def generate_response(self, user_message: str, customer_context: Dict[str, Any] = None, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Generate AI response using Groq API (free & fast!) - SYNC VERSION
        """
        # Try different models in case one is deprecated
        models_to_try = [
            "llama-3.1-8b-instant",  # Primary model
            "llama3-8b-8192",        # Fallback (in case it works for some)
            "mixtral-8x7b-32768"     # Alternative model
        ]
        
        for model in models_to_try:
            try:
                # Build the context-aware prompt
                system_prompt = self._build_system_prompt(customer_context)
                
                # Prepare messages
                messages = [{"role": "system", "content": system_prompt}]
                
                # Add conversation history if available
                if conversation_history:
                    messages.extend(conversation_history[-6:])
                
                # Add current user message
                messages.append({"role": "user", "content": user_message})
                
                # Call Groq API - SYNC version
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.groq_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 500
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data["choices"][0]["message"]["content"]
                    
                    # Analyze intent
                    intent = self._analyze_intent(user_message, ai_response)
                    
                    logger.info(f"Successfully used model: {model}")
                    return {
                        "response": ai_response,
                        "intent": intent,
                        "requires_human": self._should_escalate_to_human(intent, user_message),
                        "confidence": 0.9
                    }
                else:
                    logger.warning(f"Model {model} failed: {response.status_code}")
                    continue  # Try next model
                
            except Exception as e:
                logger.warning(f"Model {model} error: {e}")
                continue  # Try next model
        
        # If all models fail, use fallback
        logger.error("All AI models failed, using fallback response")
        return self._get_fallback_response()
    
    def _build_system_prompt(self, customer_context: Dict[str, Any] = None) -> str:
        """Build the system prompt with business context"""
        
        base_prompt = """You are a friendly and helpful customer service agent for an e-commerce store. 
Your goal is to assist customers with their inquiries in a professional, empathetic manner.

KEY RESPONSE GUIDELINES:
1. Be warm, friendly, and professional
2. If you don't have specific order data, guide customers on how to find it
3. For order status inquiries, ask for order number or email
4. For product questions, be helpful but suggest checking the website for latest inventory
5. Escalate to human agent for complex returns, complaints, or technical issues
6. Always maintain brand voice - helpful, efficient, and caring

COMMON SCENARIOS:
- Order Status: "I'd be happy to check your order status! Do you have your order number or the email used for purchase?"
- Product Info: "I can help with general product information! For specific inventory and pricing, our website has the most up-to-date details."
- Shipping: "For shipping questions, I'll need your order number to look up the latest tracking information."
- Returns: "For returns and exchanges, I'll connect you with our specialist team who can process this for you."
- General Help: "I'm here to help! What can I assist you with today?"

Always be honest about what information you have access to. If you need specific data from our systems, let the customer know what information you need to help them."""

        if customer_context:
            context_section = "\n\nCUSTOMER CONTEXT:\n"
            if customer_context.get('recent_orders'):
                context_section += f"- Recent orders: {len(customer_context['recent_orders'])} orders\n"
            if customer_context.get('customer_name'):
                context_section += f"- Customer name: {customer_context['customer_name']}\n"
            base_prompt += context_section

        return base_prompt
    
    def _analyze_intent(self, user_message: str, ai_response: str) -> str:
        """Analyze the intent of the user message"""
        message_lower = user_message.lower()
        
        intents = {
            'order_status': ['order status', 'where is my order', 'tracking', 'when will it arrive', 'order number'],
            'product_info': ['product', 'in stock', 'available', 'price', 'size', 'color'],
            'shipping': ['shipping', 'delivery', 'ship', 'arrive'],
            'returns': ['return', 'exchange', 'refund', 'send back'],
            'general_help': ['help', 'hello', 'hi', 'support', 'question']
        }
        
        for intent, keywords in intents.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent
        
        return 'general_help'
    
    def _should_escalate_to_human(self, intent: str, user_message: str) -> bool:
        """Determine if conversation should be escalated to human agent"""
        escalation_keywords = [
            'manager', 'supervisor', 'complaint', 'angry', 'furious', 
            'terrible', 'awful', 'horrible', 'cancel my account', 'legal'
        ]
        
        message_lower = user_message.lower()
        
        if intent in ['returns']:
            return True
        
        if any(keyword in message_lower for keyword in escalation_keywords):
            return True
            
        return False
    
    def _get_fallback_response(self) -> Dict[str, Any]:
        """Return a fallback response when AI service fails"""
        return {
            "response": "I'd be happy to help you with your question about blue t-shirts! For the most current inventory information, I recommend checking our website as it has real-time stock updates. Is there a specific size or style you're looking for?",
            "intent": "product_info",
            "requires_human": False,
            "confidence": 0.0
        }

# Global AI service instance
ai_service = AIService()