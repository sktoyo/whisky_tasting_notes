from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class KeywordDetail(BaseModel):
    scope: str
    term: str
    icon_key: Optional[str] = None
    detail_text: Optional[str] = None
    position: int = 0
    source_type: str = "vocabulary"


class NoteCreate(BaseModel):
    name: str
    distillery: Optional[str] = None
    age: Optional[int] = None
    cask_type: Optional[str] = None
    abv: Optional[float] = None
    is_single_cask: bool = False
    cask_info: Optional[str] = None
    bottle_remaining: Optional[str] = None
    bottle_opened_at: Optional[date] = None
    overall_comment: Optional[str] = None
    score: Optional[int] = None
    is_draft: bool = False
    keywords: list[KeywordDetail] = []


class NoteUpdate(BaseModel):
    name: Optional[str] = None
    distillery: Optional[str] = None
    age: Optional[int] = None
    cask_type: Optional[str] = None
    abv: Optional[float] = None
    is_single_cask: Optional[bool] = None
    cask_info: Optional[str] = None
    bottle_remaining: Optional[str] = None
    bottle_opened_at: Optional[date] = None
    overall_comment: Optional[str] = None
    score: Optional[int] = None
    is_draft: Optional[bool] = None
    keywords: Optional[list[KeywordDetail]] = None

