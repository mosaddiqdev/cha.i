"""Database seeding script."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, init_db
from app.models import Character
from app.characters import ALL_CHARACTERS
import json


def seed_characters():
    """Seed characters into the database."""
    db = SessionLocal()
    
    try:
        # Check if characters already exist
        existing_count = db.query(Character).count()
        if existing_count > 0:
            print(f"⚠️  Database already has {existing_count} characters. Skipping seed.")
            return
        
        # Add all characters
        for char_id, profile in ALL_CHARACTERS.items():
            char_dict = profile.to_dict()
            character = Character(
                id=char_dict["id"],
                name=char_dict["name"],
                title=char_dict["title"],
                avatar_url=char_dict["avatar_url"],
                description=char_dict["description"],
                domain=char_dict["domain"],
                personality=char_dict["personality"],
                use_cases=json.dumps(char_dict["use_cases"]),
                system_prompt=char_dict["system_prompt"]
            )
            db.add(character)
        
        db.commit()
        print(f"✅ Successfully seeded {len(ALL_CHARACTERS)} characters!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    
    print("Seeding characters...")
    seed_characters()
    
    print("✅ Database setup complete!")
