"""Simple database initialization script."""

if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    from app.core.database import SessionLocal, init_db, engine
    from app.models import Character
    from app.characters import ALL_CHARACTERS
    import json
    
    print("Initializing database...")
    init_db()
    
    db = SessionLocal()
    try:
        # Check if characters already exist
        existing_count = db.query(Character).count()
        if existing_count > 0:
            print(f"✅ Database already has {existing_count} characters.")
        else:
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
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("✅ Database setup complete!")
