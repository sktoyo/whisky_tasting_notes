from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, date
import os
import random
import json

from app.db import get_db, init_db
from app.models import Note, NoteKeyword, VocabularyTerm, UserTerm
from app.schemas import NoteCreate, NoteUpdate, KeywordDetail
from app.services.note_service import NoteService
from app.services.keyword_service import KeywordService
from app.services.featured_service import FeaturedService

app = FastAPI(title="Whisky Tasting Note MVP")

# Static files and templates
# 경로는 실행 위치에 따라 조정 (backend 디렉토리에서 실행 가정)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")
UPLOADS_DIR = os.path.join(BASE_DIR, "app", "uploads")
TEMPLATES_DIR = os.path.join(BASE_DIR, "app", "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Icon mapping function for templates
def get_icon_emoji(icon_key):
    """Convert icon_key to emoji - icon_key is already stored as emoji in database"""
    if not icon_key:
        return "🔖"
    
    # icon_key가 이미 이모지인 경우 (길이 1-2인 유니코드 문자)
    # 대부분의 이모지는 1-2자 길이입니다
    if len(icon_key) <= 2:
        return icon_key
    
    # 예상치 못한 경우 기본값 반환
    return "🔖"

# Register function in Jinja2 environment
templates.env.globals['get_icon_emoji'] = get_icon_emoji

# Create uploads directory if not exists
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    # Seed vocabulary terms if not already seeded
    from app.seed import seed_vocabulary
    seed_vocabulary()

# Featured notes cache (하루 고정 랜덤)
featured_cache = {"date": None, "notes": []}

def get_featured_notes(db: Session):
    """하루 동안 고정되는 랜덤 5건"""
    today = date.today()
    if featured_cache["date"] != today:
        featured_cache["date"] = today
        all_notes = db.query(Note).filter(Note.is_draft == False).all()
        if len(all_notes) <= 5:
            featured_cache["notes"] = [n.id for n in all_notes]
        else:
            featured_cache["notes"] = [n.id for n in random.sample(all_notes, 5)]
    return featured_cache["notes"]


# ========== SSR Routes ==========

@app.get("/", response_class=HTMLResponse)
async def board_page(
    request: Request,
    view: str = "card",
    sort_by: str = "created_at",
    sort_order: str = "desc",
    search: Optional[str] = None,
    search_mode: str = "AND",
    db: Session = Depends(get_db)
):
    """게시판 페이지"""
    # Featured notes
    featured_ids = get_featured_notes(db)
    featured_notes = db.query(Note).filter(
        Note.id.in_(featured_ids),
        Note.is_draft == False
    ).all() if featured_ids else []
    
    # Main notes query
    query = db.query(Note).filter(Note.is_draft == False)
    
    # Search
    if search:
        search_terms = [s.strip() for s in search.split() if s.strip()]
        if search_terms:
            if search_mode == "AND":
                for term in search_terms:
                    query = query.filter(
                        (Note.name.contains(term)) |
                        (Note.distillery.contains(term)) |
                        (Note.id.in_(
                            db.query(NoteKeyword.note_id).filter(
                                NoteKeyword.term.contains(term)
                            )
                        ))
                    )
            else:  # OR
                or_conditions = []
                for term in search_terms:
                    or_conditions.append(Note.name.contains(term))
                    or_conditions.append(Note.distillery.contains(term))
                    or_conditions.append(Note.id.in_(
                        db.query(NoteKeyword.note_id).filter(
                            NoteKeyword.term.contains(term)
                        )
                    ))
                from sqlalchemy import or_
                query = query.filter(or_(*or_conditions))
    
    # Sort
    if sort_by == "name":
        query = query.order_by(Note.name.asc() if sort_order == "asc" else Note.name.desc())
    else:  # created_at
        query = query.order_by(Note.created_at.asc() if sort_order == "asc" else Note.created_at.desc())
    
    notes = query.all()
    
    return templates.TemplateResponse("board.html", {
        "request": request,
        "featured_notes": featured_notes,
        "notes": notes,
        "view": view,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "search": search or "",
        "search_mode": search_mode
    })


@app.get("/notes/new", response_class=HTMLResponse)
async def create_note_page(request: Request, db: Session = Depends(get_db)):
    """노트 작성 페이지"""
    # Get vocabulary terms organized by hierarchy
    def get_hierarchical_terms(scope):
        vocab = db.query(VocabularyTerm).filter(VocabularyTerm.scope == scope).order_by(VocabularyTerm.level, VocabularyTerm.category, VocabularyTerm.subcategory).all()
        user = db.query(UserTerm).filter(UserTerm.scope == scope).all()
        
        # Organize into hierarchical structure
        hierarchy = {}
        categories = {}  # Level 1 terms
        subcategories = {}  # Level 2 terms by category
        
        for term in vocab:
            cat = term.category or "기타"
            subcat = term.subcategory or "일반"
            
            # Store category (level 1)
            if term.level == 1:
                categories[cat] = {
                    "term": term.term,
                    "icon_key": term.icon_key
                }
            
            # Store subcategory (level 2)
            if term.level == 2:
                if cat not in subcategories:
                    subcategories[cat] = {}
                subcategories[cat][subcat] = {
                    "term": term.term,
                    "icon_key": term.icon_key
                }
            
            # Organize detail keywords (level 3)
            if cat not in hierarchy:
                hierarchy[cat] = {}
            if subcat not in hierarchy[cat]:
                hierarchy[cat][subcat] = []
            
            if term.level == 3:
                # Convert VocabularyTerm to dict for JSON serialization
                hierarchy[cat][subcat].append({
                    "term": term.term,
                    "icon_key": term.icon_key
                })
        
        # Convert UserTerm to dict for JSON serialization
        user_dicts = [{"term": u.term, "icon_key": u.icon_key} for u in user]
        
        return {
            "hierarchy": hierarchy, 
            "user_terms": user_dicts,
            "categories": categories,
            "subcategories": subcategories
        }
    
    nose_data = get_hierarchical_terms("nose")
    palate_data = get_hierarchical_terms("palate")
    finish_data = get_hierarchical_terms("finish")
    
    return templates.TemplateResponse("note_form.html", {
        "request": request,
        "note": None,
        "nose_data": nose_data,
        "palate_data": palate_data,
        "finish_data": finish_data,
        "mode": "create"
    })


@app.get("/notes/{note_id}", response_class=HTMLResponse)
async def note_detail_page(
    request: Request,
    note_id: int,
    db: Session = Depends(get_db)
):
    """노트 상세 페이지"""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Get keywords grouped by scope
    keywords = db.query(NoteKeyword).filter(NoteKeyword.note_id == note_id).order_by(NoteKeyword.position).all()
    nose_keywords = [k for k in keywords if k.scope == "nose"]
    palate_keywords = [k for k in keywords if k.scope == "palate"]
    finish_keywords = [k for k in keywords if k.scope == "finish"]
    
    return templates.TemplateResponse("note_detail.html", {
        "request": request,
        "note": note,
        "nose_keywords": nose_keywords,
        "palate_keywords": palate_keywords,
        "finish_keywords": finish_keywords
    })


@app.get("/notes/{note_id}/edit", response_class=HTMLResponse)
async def edit_note_page(
    request: Request,
    note_id: int,
    db: Session = Depends(get_db)
):
    """노트 수정 페이지"""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Get keywords grouped by scope
    keywords = db.query(NoteKeyword).filter(NoteKeyword.note_id == note_id).order_by(NoteKeyword.position).all()
    nose_keywords = [{"term": k.term, "icon_key": k.icon_key, "detail_text": k.detail_text, "position": k.position, "source_type": k.source_type} for k in keywords if k.scope == "nose"]
    palate_keywords = [{"term": k.term, "icon_key": k.icon_key, "detail_text": k.detail_text, "position": k.position, "source_type": k.source_type} for k in keywords if k.scope == "palate"]
    finish_keywords = [{"term": k.term, "icon_key": k.icon_key, "detail_text": k.detail_text, "position": k.position, "source_type": k.source_type} for k in keywords if k.scope == "finish"]
    
    # Get vocabulary terms organized by hierarchy
    def get_hierarchical_terms(scope):
        vocab = db.query(VocabularyTerm).filter(VocabularyTerm.scope == scope).order_by(VocabularyTerm.level, VocabularyTerm.category, VocabularyTerm.subcategory).all()
        user = db.query(UserTerm).filter(UserTerm.scope == scope).all()
        
        # Organize into hierarchical structure
        hierarchy = {}
        for term in vocab:
            cat = term.category or "기타"
            subcat = term.subcategory or "일반"
            
            if cat not in hierarchy:
                hierarchy[cat] = {}
            if subcat not in hierarchy[cat]:
                hierarchy[cat][subcat] = []
            
            # Only add level 3 (detail keywords) to the lists
            if term.level == 3:
                # Convert VocabularyTerm to dict for JSON serialization
                hierarchy[cat][subcat].append({
                    "term": term.term,
                    "icon_key": term.icon_key
                })
        
        # Convert UserTerm to dict for JSON serialization
        user_dicts = [{"term": u.term, "icon_key": u.icon_key} for u in user]
        
        return {"hierarchy": hierarchy, "user_terms": user_dicts}
    
    nose_data = get_hierarchical_terms("nose")
    palate_data = get_hierarchical_terms("palate")
    finish_data = get_hierarchical_terms("finish")
    
    return templates.TemplateResponse("note_form.html", {
        "request": request,
        "note": note,
        "nose_keywords": nose_keywords,
        "palate_keywords": palate_keywords,
        "finish_keywords": finish_keywords,
        "nose_data": nose_data,
        "palate_data": palate_data,
        "finish_data": finish_data,
        "mode": "edit"
    })


# ========== API Routes ==========

@app.post("/api/notes")
async def create_note(
    name: str = Form(...),
    distillery: Optional[str] = Form(None),
    age: Optional[int] = Form(None),
    cask_type: Optional[str] = Form(None),
    abv: Optional[float] = Form(None),
    is_single_cask: bool = Form(False),
    cask_info: Optional[str] = Form(None),
    bottle_remaining: Optional[str] = Form(None),
    bottle_opened_at: Optional[str] = Form(None),
    nose_comment: Optional[str] = Form(None),
    palate_comment: Optional[str] = Form(None),
    finish_comment: Optional[str] = Form(None),
    overall_comment: Optional[str] = Form(None),
    score: Optional[int] = Form(None),
    is_draft: bool = Form(False),
    keywords_json: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """노트 생성"""
    # Parse keywords
    try:
        keywords_data = json.loads(keywords_json)
    except:
        keywords_data = []
    
    # Save image
    image_path = None
    if image:
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image.filename}"
        filepath = os.path.join(UPLOADS_DIR, filename)
        with open(filepath, "wb") as f:
            content = await image.read()
            f.write(content)
        image_path = filename
    
    # Parse bottle_opened_at
    bottle_opened_at_date = None
    if bottle_opened_at:
        try:
            bottle_opened_at_date = datetime.strptime(bottle_opened_at, "%Y-%m-%d").date()
        except:
            pass
    
    note = NoteService.create_note(
        db=db,
        name=name,
        distillery=distillery,
        age=age,
        cask_type=cask_type,
        abv=abv,
        is_single_cask=is_single_cask,
        cask_info=cask_info,
        bottle_remaining=bottle_remaining,
        bottle_opened_at=bottle_opened_at_date,
        nose_comment=nose_comment,
        palate_comment=palate_comment,
        finish_comment=finish_comment,
        overall_comment=overall_comment,
        score=score,
        is_draft=is_draft,
        image_path=image_path,
        keywords_data=keywords_data
    )
    
    return {"id": note.id, "message": "Note created successfully"}


@app.put("/api/notes/{note_id}")
async def update_note(
    note_id: int,
    name: str = Form(...),
    distillery: Optional[str] = Form(None),
    age: Optional[int] = Form(None),
    cask_type: Optional[str] = Form(None),
    abv: Optional[float] = Form(None),
    is_single_cask: bool = Form(False),
    cask_info: Optional[str] = Form(None),
    bottle_remaining: Optional[str] = Form(None),
    bottle_opened_at: Optional[str] = Form(None),
    nose_comment: Optional[str] = Form(None),
    palate_comment: Optional[str] = Form(None),
    finish_comment: Optional[str] = Form(None),
    overall_comment: Optional[str] = Form(None),
    score: Optional[int] = Form(None),
    is_draft: bool = Form(False),
    keywords_json: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """노트 수정"""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Parse keywords
    try:
        keywords_data = json.loads(keywords_json)
    except:
        keywords_data = []
    
    # Save image if new one uploaded
    image_path = note.image_path
    if image:
        # Delete old image if exists
        if note.image_path and os.path.exists(os.path.join(UPLOADS_DIR, note.image_path)):
            try:
                os.remove(os.path.join(UPLOADS_DIR, note.image_path))
            except:
                pass
        
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image.filename}"
        filepath = os.path.join(UPLOADS_DIR, filename)
        with open(filepath, "wb") as f:
            content = await image.read()
            f.write(content)
        image_path = filename
    
    # Parse bottle_opened_at
    bottle_opened_at_date = None
    if bottle_opened_at:
        try:
            bottle_opened_at_date = datetime.strptime(bottle_opened_at, "%Y-%m-%d").date()
        except:
            pass
    
    NoteService.update_note(
        db=db,
        note=note,
        name=name,
        distillery=distillery,
        age=age,
        cask_type=cask_type,
        abv=abv,
        is_single_cask=is_single_cask,
        cask_info=cask_info,
        bottle_remaining=bottle_remaining,
        bottle_opened_at=bottle_opened_at_date,
        nose_comment=nose_comment,
        palate_comment=palate_comment,
        finish_comment=finish_comment,
        overall_comment=overall_comment,
        score=score,
        is_draft=is_draft,
        image_path=image_path,
        keywords_data=keywords_data
    )
    
    return {"id": note.id, "message": "Note updated successfully"}


@app.delete("/api/notes/{note_id}")
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    """노트 삭제"""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Delete image if exists
    if note.image_path and os.path.exists(os.path.join(UPLOADS_DIR, note.image_path)):
        try:
            os.remove(os.path.join(UPLOADS_DIR, note.image_path))
        except:
            pass
    
    db.delete(note)
    db.commit()
    
    return {"message": "Note deleted successfully"}


@app.post("/api/keywords/custom")
async def create_custom_keyword(
    scope: str = Form(...),
    term: str = Form(...),
    icon_key: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """커스텀 키워드 생성"""
    user_term = UserTerm(scope=scope, term=term, icon_key=icon_key or "custom")
    db.add(user_term)
    db.commit()
    db.refresh(user_term)
    
    return {
        "id": user_term.id,
        "scope": user_term.scope,
        "term": user_term.term,
        "icon_key": user_term.icon_key
    }


@app.get("/notes/{note_id}/export.txt")
async def export_note(note_id: int, db: Session = Depends(get_db)):
    """노트 Export (.txt)"""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Get keywords grouped by scope
    keywords = db.query(NoteKeyword).filter(NoteKeyword.note_id == note_id).order_by(NoteKeyword.position).all()
    nose_keywords = [k for k in keywords if k.scope == "nose"]
    palate_keywords = [k for k in keywords if k.scope == "palate"]
    finish_keywords = [k for k in keywords if k.scope == "finish"]
    
    # Generate text content
    lines = []
    lines.append("=" * 50)
    lines.append(f"위스키 테이스팅 노트")
    lines.append("=" * 50)
    lines.append("")
    lines.append(f"이름: {note.name}")
    if note.distillery:
        lines.append(f"증류소: {note.distillery}")
    if note.age:
        lines.append(f"숙성년도: {note.age}년")
    if note.cask_type:
        lines.append(f"캐스크 종류: {note.cask_type}")
    if note.abv:
        lines.append(f"도수: {note.abv}%")
    if note.is_single_cask and note.cask_info:
        lines.append(f"싱글 캐스크: {note.cask_info}")
    if note.bottle_remaining:
        lines.append(f"잔여량: {note.bottle_remaining}")
    if note.bottle_opened_at:
        lines.append(f"개봉일: {note.bottle_opened_at}")
    lines.append("")
    lines.append("-" * 50)
    lines.append("Nose (향)")
    lines.append("-" * 50)
    if nose_keywords:
        lines.append("키워드:")
        for kw in nose_keywords:
            lines.append(f"• {kw.term}")
    if note.nose_comment:
        lines.append("")
        lines.append("한 줄 총평:")
        lines.append(note.nose_comment)
    if not nose_keywords and not note.nose_comment:
        lines.append("(내용 없음)")
    lines.append("")
    lines.append("-" * 50)
    lines.append("Palate (맛)")
    lines.append("-" * 50)
    if palate_keywords:
        lines.append("키워드:")
        for kw in palate_keywords:
            lines.append(f"• {kw.term}")
    if note.palate_comment:
        lines.append("")
        lines.append("한 줄 총평:")
        lines.append(note.palate_comment)
    if not palate_keywords and not note.palate_comment:
        lines.append("(내용 없음)")
    lines.append("")
    lines.append("-" * 50)
    lines.append("Finish (여운)")
    lines.append("-" * 50)
    if finish_keywords:
        lines.append("키워드:")
        for kw in finish_keywords:
            lines.append(f"• {kw.term}")
    if note.finish_comment:
        lines.append("")
        lines.append("한 줄 총평:")
        lines.append(note.finish_comment)
    if not finish_keywords and not note.finish_comment:
        lines.append("(내용 없음)")
    lines.append("")
    lines.append("-" * 50)
    lines.append("총평")
    lines.append("-" * 50)
    if note.overall_comment:
        lines.append(note.overall_comment)
    if note.score is not None:
        lines.append(f"점수: {note.score}/100")
    lines.append("")
    lines.append(f"작성일: {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 50)
    
    content = "\n".join(lines)
    
    # Save to temporary file
    filename = f"note_{note_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(UPLOADS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    return FileResponse(
        filepath,
        media_type="text/plain",
        filename=f"{note.name.replace(' ', '_')}_tasting_note.txt"
    )

