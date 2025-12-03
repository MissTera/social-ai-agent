import logging
import random
import time
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class SocialSimulator:
    """Simulate Instagram & WhatsApp for investor demos"""
    
    def __init__(self):
        self.conversations = {}
        self.demo_users = [
            {"id": "ig_customer_001", "name": "Sarah M.", "platform": "instagram", "avatar": "👩‍💼"},
            {"id": "wa_customer_002", "name": "Mike T.", "platform": "whatsapp", "avatar": "👨‍💻"},
            {"id": "ig_customer_003", "name": "Alex J.", "platform": "instagram", "avatar": "👩‍🎨"},
            {"id": "wa_customer_004", "name": "David L.", "platform": "whatsapp", "avatar": "👨‍🔧"}
        ]
    
    def simulate_incoming_message(self, platform: str = None) -> Dict:
        """Simulate a customer sending a message"""
        if not platform:
            platform = random.choice(["instagram", "whatsapp"])
        
        user = random.choice([u for u in self.demo_users if u["platform"] == platform])
        
        # Common customer questions
        questions = [
            "Where is my order #ORD12345?",
            "Do you have this in blue?",
            "What's your return policy?",
            "How long does shipping take?",
            "Do you ship to Canada?",
            "My order arrived damaged, what should I do?",
            "What's the estimated delivery time?",
            "Can I change my shipping address?",
            "Do you have size guides?",
            "Is this product in stock?"
        ]
        
        message = {
            "platform": platform,
            "user_id": user["id"],
            "user_name": user["name"],
            "user_avatar": user["avatar"],
            "message": random.choice(questions),
            "timestamp": datetime.now().isoformat(),
            "simulated": True
        }
        
        # Store in conversation history
        if user["id"] not in self.conversations:
            self.conversations[user["id"]] = []
        self.conversations[user["id"]].append({
            "type": "customer",
            "message": message["message"],
            "timestamp": message["timestamp"]
        })
        
        logger.info(f"[SIM] {user['avatar']} {user['name']} ({platform}): {message['message']}")
        return message
    
    def simulate_ai_response(self, user_id: str, ai_response: str) -> Dict:
        """Simulate AI sending response back"""
        user = next((u for u in self.demo_users if u["id"] == user_id), None)
        if not user:
            user = {"id": user_id, "name": "Customer", "platform": "unknown", "avatar": "👤"}
        
        response = {
            "platform": user["platform"],
            "user_id": user["id"],
            "user_name": "AI Assistant",
            "user_avatar": "🤖",
            "message": ai_response,
            "timestamp": datetime.now().isoformat(),
            "simulated": True
        }
        
        # Store AI response
        if user["id"] in self.conversations:
            self.conversations[user["id"]].append({
                "type": "ai",
                "message": ai_response,
                "timestamp": response["timestamp"]
            })
        
        logger.info(f"[SIM] 🤖 AI ({user['platform']}): {ai_response[:50]}...")
        return response
    
    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """Get simulated conversation history"""
        return self.conversations.get(user_id, [])
    
    def get_demo_statistics(self) -> Dict:
        """Get demo statistics for investor dashboard"""
        total_messages = sum(len(conv) for conv in self.conversations.values())
        return {
            "total_conversations": len(self.conversations),
            "total_messages": total_messages,
            "platforms": {
                "instagram": len([u for u in self.demo_users if u["platform"] == "instagram"]),
                "whatsapp": len([u for u in self.demo_users if u["platform"] == "whatsapp"])
            },
            "active_demo_users": self.demo_users
        }

# Global simulator instance
social_simulator = SocialSimulator()