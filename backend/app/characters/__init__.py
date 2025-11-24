
from app.characters.mira import mira_profile
from app.characters.ethan import ethan_profile
from app.characters.kai import kai_profile
from app.characters.ivy import ivy_profile
from app.characters.marcus import marcus_profile

ALL_CHARACTERS = {
    "mira": mira_profile,
    "ethan": ethan_profile,
    "kai": kai_profile,
    "ivy": ivy_profile,
    "marcus": marcus_profile
}

def get_character_profile(character_id: str):
    return ALL_CHARACTERS.get(character_id)

__all__ = [
    "ALL_CHARACTERS",
    "get_character_profile",
    "mira_profile",
    "ethan_profile",
    "kai_profile",
    "ivy_profile",
    "marcus_profile"
]
