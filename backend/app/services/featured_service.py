from datetime import date
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models import Note


class FeaturedService:
    """하루 동안 고정되는 랜덤 추천 노트 관리"""
    
    _cache: Dict[str, List[int]] = {}
    
    @classmethod
    def get_featured_notes(cls, db: Session, count: int = 5) -> List[Note]:
        """Get featured notes for today (cached for the day)"""
        today = date.today().isoformat()
        
        if today not in cls._cache:
            # Get all non-draft notes
            all_notes = db.query(Note).filter(Note.is_draft == False).all()
            
            if len(all_notes) <= count:
                note_ids = [n.id for n in all_notes]
            else:
                import random
                note_ids = [n.id for n in random.sample(all_notes, count)]
            
            cls._cache[today] = note_ids
        
        note_ids = cls._cache[today]
        return db.query(Note).filter(Note.id.in_(note_ids)).all() if note_ids else []

