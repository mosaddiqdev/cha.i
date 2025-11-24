"""Chat routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse, ConversationResponse, MessageResponse
from app.services.ai_service import ai_service
from app.services.conversation_service import conversation_service
from app.services.rag_service import rag_service
from app.services.summarization_service import summarization_service
from app.services.preference_service import preference_service
from app.characters import get_character_profile
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def send_message(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Send a message to a character and get a response with Phase 2 enhancements.
    
    Features:
    - RAG: Retrieves relevant context from past conversations
    - Summarization: Auto-summarizes long conversations
    - User Preferences: Tracks and uses user preferences
    - Sentiment Analysis: Adapts to user's emotional state
    """
    # Get character profile
    character_profile = get_character_profile(request.character_id)
    if not character_profile:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # Get or create conversation
    if request.conversation_id:
        conversation = conversation_service.get_conversation(db, request.conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        # Create new conversation
        conversation = conversation_service.create_conversation(
            db,
            character_id=request.character_id,
            user_id=request.user_id or "anonymous"
        )
    
    # Save user message
    user_msg = conversation_service.add_message(
        db,
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    
    # Get conversation history
    history = conversation_service.get_conversation_history(db, conversation.id)
    
    # === PHASE 2 ENHANCEMENTS ===
    
    # 1. Check if summarization is needed
    summary = ""
    if summarization_service.should_summarize(db, conversation.id):
        summary = summarization_service.create_progressive_summary(db, conversation.id)
    else:
        summary = summarization_service.get_conversation_summary(db, conversation.id)
    
    # 2. RAG: Retrieve relevant context from past conversations
    rag_context = rag_service.retrieve_relevant_context(
        user_message=request.message,
        user_id=request.user_id or "anonymous",
        character_id=request.character_id,
        current_conversation_id=conversation.id,
        n_results=3
    )
    
    # 3. Get user preferences
    user_profile = preference_service.get_user_profile(
        db,
        user_id=request.user_id or "anonymous",
        character_id=request.character_id
    )
    
    # 4. Analyze sentiment
    sentiment = preference_service.analyze_sentiment(request.message)
    
    # Build enhanced prompt
    system_prompt = character_profile.build_system_prompt()
    
    # Add Phase 2 context
    enhanced_context = []
    if summary:
        enhanced_context.append(f"CONVERSATION SUMMARY:\n{summary}")
    if rag_context:
        enhanced_context.append(rag_context)
    if user_profile:
        enhanced_context.append(user_profile)
    if sentiment.get('emotion') != 'calm':
        enhanced_context.append(f"USER EMOTIONAL STATE: {sentiment.get('emotion')} ({sentiment.get('sentiment')})")
    
    if enhanced_context:
        system_prompt += "\n\n" + "\n\n".join(enhanced_context)
    
    # Generate AI response
    ai_response = ai_service.generate_response(
        system_prompt=system_prompt,
        conversation_history=history[:-1],  # Exclude the just-added user message
        user_message=request.message
    )
    
    # Save AI response
    ai_msg = conversation_service.add_message(
        db,
        conversation_id=conversation.id,
        role="character",
        content=ai_response
    )
    
    # === POST-RESPONSE PHASE 2 TASKS ===
    
    # 5. Index messages in RAG vector store
    rag_service.index_message(
        message_id=user_msg.id,
        conversation_id=conversation.id,
        user_id=request.user_id or "anonymous",
        character_id=request.character_id,
        role="user",
        content=request.message,
        timestamp=user_msg.timestamp
    )
    rag_service.index_message(
        message_id=ai_msg.id,
        conversation_id=conversation.id,
        user_id=request.user_id or "anonymous",
        character_id=request.character_id,
        role="character",
        content=ai_response,
        timestamp=ai_msg.timestamp
    )
    
    # 6. Extract and update user preferences (every 5 messages)
    if len(history) % 5 == 0:
        preference_service.extract_preferences(
            db,
            messages=[user_msg, ai_msg],
            user_id=request.user_id or "anonymous",
            character_id=request.character_id
        )
    
    # Generate title if first message
    if len(history) == 1:
        title = ai_service.generate_conversation_title(request.message)
        conversation_service.update_conversation_title(db, conversation.id, title)
    
    return ChatResponse(
        conversation_id=conversation.id,
        character_response=ai_response,
        timestamp=datetime.utcnow(),
        metadata={
            "rag_used": bool(rag_context),
            "summary_available": bool(summary),
            "user_profile_used": bool(user_profile),
            "sentiment": sentiment
        }
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """Get a conversation with all its messages."""
    conversation = conversation_service.get_conversation(db, conversation_id)
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = [
        MessageResponse(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            timestamp=msg.timestamp
        )
        for msg in conversation.messages
    ]
    
    return ConversationResponse(
        id=conversation.id,
        character_id=conversation.character_id,
        title=conversation.title,
        started_at=conversation.started_at,
        last_message_at=conversation.last_message_at,
        messages=messages
    )


class ClearMemoryRequest(BaseModel):
    character_id: str
    user_id: str


@router.post("/chat/clear")
def clear_memory(request: ClearMemoryRequest, db: Session = Depends(get_db)):
    conversation = conversation_service.get_active_conversation(
        db, request.user_id, request.character_id
    )
    
    if conversation:
        db.delete(conversation)
        db.commit()
        
        return {"status": "success", "message": "Memory cleared"}
    
    return {"status": "success", "message": "No active conversation found"}
