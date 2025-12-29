from sqlalchemy.orm import Session
from app.models import VocabularyTerm, UserTerm


class KeywordService:
    @staticmethod
    def get_vocabulary_terms(db: Session, scope: str):
        """Get vocabulary terms for a scope"""
        return db.query(VocabularyTerm).filter(VocabularyTerm.scope == scope).all()
    
    @staticmethod
    def get_user_terms(db: Session, scope: str = None):
        """Get user terms, optionally filtered by scope"""
        query = db.query(UserTerm)
        if scope:
            query = query.filter(UserTerm.scope == scope)
        return query.all()
    
    @staticmethod
    def create_user_term(db: Session, scope: str, term: str, icon_key: str = "custom"):
        """Create a new user term"""
        user_term = UserTerm(scope=scope, term=term, icon_key=icon_key)
        db.add(user_term)
        db.commit()
        db.refresh(user_term)
        return user_term

