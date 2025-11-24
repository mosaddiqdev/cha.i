import logging
import json
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.character import Character
from app.characters import ALL_CHARACTERS

logger = logging.getLogger(__name__)

def seed_data():
    """Seeds the database with initial data from app.characters if empty."""
    db: Session = SessionLocal()
    try:
        # Check if characters exist
        if db.query(Character).first():
            logger.info("✅ Database already seeded.")
            return

        logger.info(f"🌱 Seeding database with {len(ALL_CHARACTERS)} characters...")
        
        for char_id, profile in ALL_CHARACTERS.items():
            char_dict = profile.to_dict()
            
            # Ensure use_cases is JSON string if it's a list/dict
            use_cases_val = char_dict.get("use_cases")
            if isinstance(use_cases_val, (list, dict)):
                use_cases_val = json.dumps(use_cases_val)
            
            character = Character(
                id=char_dict["id"],
                name=char_dict["name"],
                title=char_dict["title"],
                avatar_url=char_dict["avatar_url"],
                description=char_dict["description"],
                domain=char_dict["domain"],
                personality=char_dict["personality"],
                use_cases=use_cases_val,
                system_prompt=char_dict["system_prompt"]
            )
            db.add(character)
        
        db.commit()
        logger.info("✅ Database seeding completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()
