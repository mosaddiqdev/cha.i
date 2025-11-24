
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Character
from app.schemas.chat import CharacterResponse
from app.characters import ALL_CHARACTERS
from typing import List
import json

router = APIRouter(prefix="/api/characters", tags=["characters"])


@router.get("", response_model=List[CharacterResponse])
def get_all_characters(db: Session = Depends(get_db)):
    characters = db.query(Character).all()
    
    return [
        CharacterResponse(
            id=char.id,
            name=char.name,
            title=char.title,
            image=char.avatar_url,
            description=char.description,
            domain=char.domain,
            personality=char.personality,
            useCases=json.loads(char.use_cases) if char.use_cases else []
        )
        for char in characters
    ]


@router.get("/{character_id}", response_model=CharacterResponse)
def get_character(character_id: str, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    return CharacterResponse(
        id=character.id,
        name=character.name,
        title=character.title,
        image=character.avatar_url,
        description=character.description,
        domain=character.domain,
        personality=character.personality,
        useCases=json.loads(character.use_cases) if character.use_cases else []
    )
