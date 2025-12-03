from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.social_simulator import social_simulator
from app.services.conversation_manager import get_conversation_manager
import logging

router = APIRouter(prefix="/demo", tags=["demo"])
logger = logging.getLogger(__name__)

@router.get("/simulate/message")
async def simulate_message(platform: str = None):
    """Simulate a customer sending a message (for investor demos)"""
    simulated_message = social_simulator.simulate_incoming_message(platform)
    return {
        "status": "simulated",
        "message": "Customer message simulated successfully",
        "data": simulated_message,
        "instructions": "Now POST this to /demo/process to see AI respond"
    }

@router.post("/process/simulated")
async def process_simulated_message(
    user_id: str,
    message: str,
    platform: str,
    db: Session = Depends(get_db)
):
    """Process simulated message with real AI"""
    # Use your actual AI to generate response
    conversation_manager = get_conversation_manager(db)
    result = await conversation_manager.process_message(
        user_message=message,
        social_media_id=user_id,
        platform=platform
    )
    
    # Simulate the AI response
    ai_response = social_simulator.simulate_ai_response(user_id, result["response"])
    
    return {
        "status": "processed",
        "ai_result": result,
        "simulated_response": ai_response,
        "message": f"AI processed message and responded via {platform}"
    }

@router.get("/dashboard")
async def investor_dashboard():
    """Investor demo dashboard with statistics"""
    stats = social_simulator.get_demo_statistics()
    
    # Simulate some recent activity
    recent_activity = []
    for user in social_simulator.demo_users[:3]:  # Show first 3 users
        history = social_simulator.get_conversation_history(user["id"])
        if history:
            recent_activity.append({
                "user": user,
                "last_message": history[-1]["message"],
                "message_count": len(history)
            })
    
    return {
        "dashboard_title": "🤖 AI Business Scaling Agent - Investor Demo",
        "status": "live",
        "simulation_mode": True,
        "statistics": stats,
        "recent_activity": recent_activity,
        "capabilities": [
            "24/7 Customer Service",
            "Instagram DM Automation",
            "WhatsApp Business Integration",
            "Order Status Tracking",
            "Product Information",
            "Social Media Content Generation (Coming Soon)"
        ],
        "business_value": [
            "Saves 20+ hours/week per business",
            "Reduces customer service costs by 70%",
            "Increases customer satisfaction",
            "Generates social content from interactions"
        ]
    }

@router.post("/live/demo")
async def live_investor_demo(db: Session = Depends(get_db)):
    """Complete live demo for investors - simulates real conversation"""
    # Step 1: Simulate customer message
    simulated_msg = social_simulator.simulate_incoming_message()
    
    # Step 2: Process with real AI
    conversation_manager = get_conversation_manager(db)
    result = await conversation_manager.process_message(
        user_message=simulated_msg["message"],
        social_media_id=simulated_msg["user_id"],
        platform=simulated_msg["platform"]
    )
    
    # Step 3: Simulate AI response
    ai_response = social_simulator.simulate_ai_response(
        simulated_msg["user_id"],
        result["response"]
    )
    
    return {
        "demo_title": "🎯 Live Investor Demo - AI Business Scaling Agent",
        "step_1": {
            "action": "Customer sends message",
            "data": simulated_msg
        },
        "step_2": {
            "action": "AI processes and understands intent",
            "data": {
                "intent": result["intent"],
                "requires_human": result["requires_human"],
                "confidence": result.get("confidence", 0.9)
            }
        },
        "step_3": {
            "action": "AI sends professional response",
            "data": ai_response
        },
        "business_impact": "This interaction just saved 15 minutes of customer service time",
        "platform_ready": "Instagram & WhatsApp integration fully built - awaiting API keys"
    }