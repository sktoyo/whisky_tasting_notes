from sqlalchemy import Column, Integer, String, Float, Boolean, Text, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    distillery = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    cask_type = Column(String, nullable=True)
    abv = Column(Float, nullable=True)
    is_single_cask = Column(Boolean, default=False)
    cask_info = Column(String, nullable=True)
    bottle_remaining = Column(String, nullable=True)
    bottle_opened_at = Column(Date, nullable=True)
    nose_comment = Column(Text, nullable=True)
    palate_comment = Column(Text, nullable=True)
    finish_comment = Column(Text, nullable=True)
    overall_comment = Column(Text, nullable=True)
    score = Column(Integer, nullable=True)
    image_path = Column(String, nullable=True)
    is_draft = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    keywords = relationship("NoteKeyword", back_populates="note", cascade="all, delete-orphan")


class NoteKeyword(Base):
    __tablename__ = "note_keywords"
    
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=False)
    scope = Column(String, nullable=False)  # nose, palate, finish
    term = Column(String, nullable=False)
    icon_key = Column(String, nullable=True)
    detail_text = Column(Text, nullable=True)
    position = Column(Integer, default=0)
    source_type = Column(String, default="vocabulary")  # vocabulary, user
    
    note = relationship("Note", back_populates="keywords")


class VocabularyTerm(Base):
    __tablename__ = "vocabulary_terms"
    __table_args__ = (
        # (scope, term) 조합이 unique하도록 설정
        # 같은 term이 여러 scope에 나타날 수 있음
        UniqueConstraint('scope', 'term', name='uix_scope_term'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    scope = Column(String, nullable=False, index=True)  # nose, palate, finish
    term = Column(String, nullable=False, index=True)
    icon_key = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserTerm(Base):
    __tablename__ = "user_terms"
    
    id = Column(Integer, primary_key=True, index=True)
    scope = Column(String, nullable=False)  # nose, palate, finish
    term = Column(String, nullable=False)
    icon_key = Column(String, nullable=True)
    created_by = Column(String, nullable=True)  # 미래 대비
    created_at = Column(DateTime, default=datetime.utcnow)

