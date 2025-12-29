from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Dict, Any
from app.models import Note, NoteKeyword


class NoteService:
    @staticmethod
    def create_note(
        db: Session,
        name: str,
        distillery: str = None,
        age: int = None,
        cask_type: str = None,
        abv: float = None,
        is_single_cask: bool = False,
        cask_info: str = None,
        bottle_remaining: str = None,
        bottle_opened_at = None,
        nose_comment: str = None,
        palate_comment: str = None,
        finish_comment: str = None,
        overall_comment: str = None,
        score: int = None,
        is_draft: bool = False,
        image_path: str = None,
        keywords_data: List[Dict[str, Any]] = None
    ) -> Note:
        """Create a new note with keywords"""
        note = Note(
            name=name,
            distillery=distillery,
            age=age,
            cask_type=cask_type,
            abv=abv,
            is_single_cask=is_single_cask,
            cask_info=cask_info,
            bottle_remaining=bottle_remaining,
            bottle_opened_at=bottle_opened_at,
            nose_comment=nose_comment,
            palate_comment=palate_comment,
            finish_comment=finish_comment,
            overall_comment=overall_comment,
            score=score,
            is_draft=is_draft,
            image_path=image_path
        )
        db.add(note)
        db.flush()
        
        # Add keywords
        if keywords_data:
            for idx, kw_data in enumerate(keywords_data):
                keyword = NoteKeyword(
                    note_id=note.id,
                    scope=kw_data.get("scope", ""),
                    term=kw_data.get("term", ""),
                    icon_key=kw_data.get("icon_key"),
                    detail_text=kw_data.get("detail_text"),
                    position=kw_data.get("position", idx),
                    source_type=kw_data.get("source_type", "vocabulary")
                )
                db.add(keyword)
        
        db.commit()
        db.refresh(note)
        return note
    
    @staticmethod
    def update_note(
        db: Session,
        note: Note,
        name: str = None,
        distillery: str = None,
        age: int = None,
        cask_type: str = None,
        abv: float = None,
        is_single_cask: bool = None,
        cask_info: str = None,
        bottle_remaining: str = None,
        bottle_opened_at = None,
        nose_comment: str = None,
        palate_comment: str = None,
        finish_comment: str = None,
        overall_comment: str = None,
        score: int = None,
        is_draft: bool = None,
        image_path: str = None,
        keywords_data: List[Dict[str, Any]] = None
    ) -> Note:
        """Update a note and its keywords"""
        if name is not None:
            note.name = name
        if distillery is not None:
            note.distillery = distillery
        if age is not None:
            note.age = age
        if cask_type is not None:
            note.cask_type = cask_type
        if abv is not None:
            note.abv = abv
        if is_single_cask is not None:
            note.is_single_cask = is_single_cask
        if cask_info is not None:
            note.cask_info = cask_info
        if bottle_remaining is not None:
            note.bottle_remaining = bottle_remaining
        if bottle_opened_at is not None:
            note.bottle_opened_at = bottle_opened_at
        if nose_comment is not None:
            note.nose_comment = nose_comment
        if palate_comment is not None:
            note.palate_comment = palate_comment
        if finish_comment is not None:
            note.finish_comment = finish_comment
        if overall_comment is not None:
            note.overall_comment = overall_comment
        if score is not None:
            note.score = score
        if is_draft is not None:
            note.is_draft = is_draft
        if image_path is not None:
            note.image_path = image_path
        
        note.updated_at = datetime.utcnow()
        
        # Delete existing keywords
        db.query(NoteKeyword).filter(NoteKeyword.note_id == note.id).delete()
        
        # Add new keywords
        if keywords_data:
            for idx, kw_data in enumerate(keywords_data):
                keyword = NoteKeyword(
                    note_id=note.id,
                    scope=kw_data.get("scope", ""),
                    term=kw_data.get("term", ""),
                    icon_key=kw_data.get("icon_key"),
                    detail_text=kw_data.get("detail_text"),
                    position=kw_data.get("position", idx),
                    source_type=kw_data.get("source_type", "vocabulary")
                )
                db.add(keyword)
        
        db.commit()
        db.refresh(note)
        return note

