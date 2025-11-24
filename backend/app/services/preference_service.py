from typing import List, Dict
from sqlalchemy.orm import Session
from app.models import UserPreference, Message
from app.services.ai_service import ai_service
import json


class PreferenceService:
    
    def extract_preferences(
        self,
        db: Session,
        messages: List[Message],
        user_id: str,
        character_id: str
    ):
        if not messages or len(messages) < 2:
            return
        
        conversation_text = "\n".join([
            f"[{msg.role.upper()}]: {msg.content}"
            for msg in messages
        ])
        
        prompt = f"""Analyze this conversation and extract user preferences.

CONVERSATION:
{conversation_text}

Extract preferences in these categories:
- topics: What topics is the user interested in?
- tone: What communication style do they prefer?
- interests: What are their hobbies or interests?

Return as JSON:
{{
  "topics": ["topic1", "topic2"],
  "tone": "casual/formal/friendly",
  "interests": ["interest1", "interest2"]
}}

JSON:"""
        
        try:
            response = ai_service.model.generate_content(prompt).text.strip()
            if '{' in response:
                json_start = response.index('{')
                json_end = response.rindex('}') + 1
                preferences = json.loads(response[json_start:json_end])
                
                for pref_type, values in preferences.items():
                    if isinstance(values, list):
                        for value in values:
                            self.update_preference(
                                db, user_id, character_id,
                                pref_type, value, value, 0.7
                            )
                    else:
                        self.update_preference(
                            db, user_id, character_id,
                            pref_type, pref_type, str(values), 0.7
                        )
        except Exception as e:
            print(f"Error extracting preferences: {e}")
    
    def update_preference(
        self,
        db: Session,
        user_id: str,
        character_id: str,
        preference_type: str,
        key: str,
        value: str,
        confidence: float
    ):
        existing = db.query(UserPreference).filter(
            UserPreference.user_id == user_id,
            UserPreference.character_id == character_id,
            UserPreference.preference_type == preference_type,
            UserPreference.preference_key == key
        ).first()
        
        if existing:
            existing.preference_value = value
            existing.confidence = min(existing.confidence + 0.1, 1.0)
        else:
            pref = UserPreference(
                user_id=user_id,
                character_id=character_id,
                preference_type=preference_type,
                preference_key=key,
                preference_value=value,
                confidence=confidence
            )
            db.add(pref)
        
        db.commit()
    
    def get_user_profile(
        self,
        db: Session,
        user_id: str,
        character_id: str
    ) -> str:
        preferences = db.query(UserPreference).filter(
            UserPreference.user_id == user_id,
            UserPreference.character_id == character_id,
            UserPreference.confidence >= 0.5
        ).all()
        
        if not preferences:
            return ""
        
        grouped = {}
        for pref in preferences:
            if pref.preference_type not in grouped:
                grouped[pref.preference_type] = []
            grouped[pref.preference_type].append(pref.preference_value)
        
        profile_parts = ["USER PROFILE:"]
        for pref_type, values in grouped.items():
            profile_parts.append(f"- {pref_type.title()}: {', '.join(values)}")
        
        return "\n".join(profile_parts)
    
    def analyze_sentiment(self, message: str) -> Dict:
        prompt = f"""Analyze the sentiment and emotion in this message:
"{message}"

Return JSON:
{{
  "sentiment": "positive/neutral/negative",
  "emotion": "happy/sad/angry/excited/stressed/calm/confused",
  "intensity": 0.0-1.0
}}

JSON:"""
        
        try:
            response = ai_service.model.generate_content(prompt).text.strip()
            if '{' in response:
                json_start = response.index('{')
                json_end = response.rindex('}') + 1
                return json.loads(response[json_start:json_end])
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
        
        return {
            "sentiment": "neutral",
            "emotion": "calm",
            "intensity": 0.5
        }


preference_service = PreferenceService()
