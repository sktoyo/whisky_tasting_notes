"""
Seed script for initial vocabulary terms
Run: python -m backend.app.seed
"""
from app.db import SessionLocal, init_db
from app.models import VocabularyTerm
from datetime import datetime


def seed_vocabulary():
    """Seed vocabulary terms for nose, palate, finish"""
    db = SessionLocal()
    
    try:
        # Get existing terms to avoid duplicates
        existing_terms = {(term.scope, term.term) for term in db.query(VocabularyTerm).all()}
        
        # Nose terms (향)
        nose_terms = [
            {"term": "바닐라", "icon_key": "vanilla"},
            {"term": "오크", "icon_key": "oak"},
            {"term": "과일", "icon_key": "fruit"},
            {"term": "꽃", "icon_key": "flower"},
            {"term": "허브", "icon_key": "herb"},
            {"term": "스파이스", "icon_key": "spice"},
            {"term": "꿀", "icon_key": "honey"},
            {"term": "초콜릿", "icon_key": "chocolate"},
            {"term": "커피", "icon_key": "coffee"},
            {"term": "시트러스", "icon_key": "citrus"},
            {"term": "피트", "icon_key": "peat"},
            {"term": "바다", "icon_key": "sea"},
            {"term": "흙", "icon_key": "earth"},
            {"term": "담배", "icon_key": "tobacco"},
            {"term": "견과류", "icon_key": "nut"},
            {"term": "카라멜", "icon_key": "caramel"},
            {"term": "말린 과일", "icon_key": "dried_fruit"},
            {"term": "향신료", "icon_key": "spice"},
            {"term": "꽃꿀", "icon_key": "honey"},
            {"term": "나무", "icon_key": "wood"},
        ]
        
        # Palate terms (맛)
        palate_terms = [
            {"term": "달콤함", "icon_key": "sweet"},
            {"term": "쓴맛", "icon_key": "bitter"},
            {"term": "신맛", "icon_key": "sour"},
            {"term": "짠맛", "icon_key": "salty"},
            {"term": "바닐라", "icon_key": "vanilla"},
            {"term": "과일", "icon_key": "fruit"},
            {"term": "초콜릿", "icon_key": "chocolate"},
            {"term": "커피", "icon_key": "coffee"},
            {"term": "스파이스", "icon_key": "spice"},
            {"term": "오크", "icon_key": "oak"},
            {"term": "피트", "icon_key": "peat"},
            {"term": "허브", "icon_key": "herb"},
            {"term": "견과류", "icon_key": "nut"},
            {"term": "카라멜", "icon_key": "caramel"},
            {"term": "꿀", "icon_key": "honey"},
            {"term": "시트러스", "icon_key": "citrus"},
            {"term": "말린 과일", "icon_key": "dried_fruit"},
            {"term": "향신료", "icon_key": "spice"},
            {"term": "부드러움", "icon_key": "smooth"},
            {"term": "강렬함", "icon_key": "intense"},
        ]
        
        # Finish terms (여운)
        finish_terms = [
            {"term": "긴 여운", "icon_key": "long"},
            {"term": "짧은 여운", "icon_key": "short"},
            {"term": "따뜻함", "icon_key": "warm"},
            {"term": "시원함", "icon_key": "cool"},
            {"term": "스파이시", "icon_key": "spice"},
            {"term": "부드러움", "icon_key": "smooth"},
            {"term": "강렬함", "icon_key": "intense"},
            {"term": "오크", "icon_key": "oak"},
            {"term": "피트", "icon_key": "peat"},
            {"term": "과일", "icon_key": "fruit"},
            {"term": "바닐라", "icon_key": "vanilla"},
            {"term": "초콜릿", "icon_key": "chocolate"},
            {"term": "커피", "icon_key": "coffee"},
            {"term": "허브", "icon_key": "herb"},
            {"term": "견과류", "icon_key": "nut"},
            {"term": "카라멜", "icon_key": "caramel"},
            {"term": "꿀", "icon_key": "honey"},
            {"term": "시트러스", "icon_key": "citrus"},
            {"term": "담배", "icon_key": "tobacco"},
            {"term": "향신료", "icon_key": "spice"},
        ]
        
        # Insert nose terms (skip if already exists)
        nose_added = 0
        for term_data in nose_terms:
            if ("nose", term_data["term"]) not in existing_terms:
                try:
                    vocab = VocabularyTerm(
                        scope="nose",
                        term=term_data["term"],
                        icon_key=term_data["icon_key"]
                    )
                    db.add(vocab)
                    db.flush()  # 즉시 DB에 반영하여 중복 확인
                    nose_added += 1
                except Exception as e:
                    db.rollback()
                    print(f"Warning: Failed to add nose term '{term_data['term']}': {e}")
                    # 이미 존재하는 경우 건너뜀
                    continue
        
        # Insert palate terms (skip if already exists)
        palate_added = 0
        for term_data in palate_terms:
            if ("palate", term_data["term"]) not in existing_terms:
                try:
                    vocab = VocabularyTerm(
                        scope="palate",
                        term=term_data["term"],
                        icon_key=term_data["icon_key"]
                    )
                    db.add(vocab)
                    db.flush()
                    palate_added += 1
                except Exception as e:
                    db.rollback()
                    print(f"Warning: Failed to add palate term '{term_data['term']}': {e}")
                    continue
        
        # Insert finish terms (skip if already exists)
        finish_added = 0
        for term_data in finish_terms:
            if ("finish", term_data["term"]) not in existing_terms:
                try:
                    vocab = VocabularyTerm(
                        scope="finish",
                        term=term_data["term"],
                        icon_key=term_data["icon_key"]
                    )
                    db.add(vocab)
                    db.flush()
                    finish_added += 1
                except Exception as e:
                    db.rollback()
                    print(f"Warning: Failed to add finish term '{term_data['term']}': {e}")
                    continue
        
        if nose_added > 0 or palate_added > 0 or finish_added > 0:
            db.commit()
            print(f"Seeded vocabulary terms: {nose_added} nose, {palate_added} palate, {finish_added} finish")
        else:
            print("All vocabulary terms already exist. No new terms added.")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding vocabulary: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Seeding vocabulary terms...")
    seed_vocabulary()
    print("Done!")

