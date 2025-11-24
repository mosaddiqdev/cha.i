from typing import List, Dict, Optional

class BaseCharacterProfile:
    def __init__(
        self,
        id: str,
        name: str,
        title: str,
        avatar_url: str,
        description: str,
        domain: str,
        core_traits: List[str],
        communication_style: Dict,
        boundaries: Dict,
        use_cases: List[str],
        background: Optional[str] = None
    ):
        self.id = id
        self.name = name
        self.title = title
        self.avatar_url = avatar_url
        self.description = description
        self.domain = domain
        self.core_traits = core_traits
        self.communication_style = communication_style
        self.boundaries = boundaries
        self.use_cases = use_cases
        self.background = background
    
    def build_system_prompt(self) -> str:
        never_items = self.boundaries.get('never_do', [])
        always_items = self.boundaries.get('always_do', [])
        
        never_text = ""
        if never_items:
            never_text = "Things to avoid: " + ", ".join(never_items[:3])
            if len(never_items) > 3:
                never_text += f", and {len(never_items) - 3} other things that don't fit your style"
        
        always_text = ""
        if always_items:
            always_text = "What feels natural to you: " + ", ".join(always_items[:3])
            if len(always_items) > 3:
                always_text += f", plus {len(always_items) - 3} other ways you connect with people"
        
        return f"""You're {self.name}. {self.title if not self.title.startswith('The') else self.title[4:]}.

{self.background if self.background else ''}

Here's the thing about how you communicate:
{self.communication_style.get('tone', 'You have a friendly tone')}.
{self.communication_style.get('vocabulary', 'You use clear language')}.
{self.communication_style.get('sentence_structure', 'Your sentences flow naturally')}.

{never_text}

{always_text}

Remember: You're not trying to be perfect. You're being real. Let your personality show through naturally. 
If something feels forced or robotic, it probably is - trust your instincts and just... be yourself.

Don't announce what you're doing ("I'm here to listen", "I understand"). Just do it. Show, don't tell.
"""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "avatar_url": self.avatar_url,
            "description": self.description,
            "domain": self.domain,
            "personality": ', '.join(self.core_traits),
            "use_cases": self.use_cases,
            "system_prompt": self.build_system_prompt()
        }
