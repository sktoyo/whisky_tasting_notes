"""
Seed script for initial vocabulary terms based on Flavor Wheel hierarchy
Run: python -m backend.app.seed
"""
import json
import os
from app.db import SessionLocal, init_db
from app.models import VocabularyTerm
from datetime import datetime


def load_flavor_categories():
    """Load flavor categories from JSON file"""
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "docs", "flavor_category.json"
    )
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_korean_translation():
    """Get Korean translations for English keywords"""
    return {
        # Categories (Level 1)
        "FRUITY": "과일향",
        "FLORAL": "꽃향",
        "SWEET": "단맛",
        "NUTTY": "견과류",
        "SPICY": "향신료",
        "SAVORY": "고소한",
        
        # Subcategories (Level 2)
        "BERRY": "베리류",
        "DRIED FRUIT": "말린 과일",
        "CITRUS": "시트러스",
        "OTHER FRUIT": "기타 과일",
        "BLACK TEA": "홍차",
        "FLORAL (GENERAL)": "꽃향 (일반)",
        "JASMINE": "자스민",
        "ROSE": "장미",
        "BROWN SUGAR": "흑설탕",
        "HONEY": "꿀",
        "MOLASSES": "당밀",
        "VANILLA": "바닐라",
        "NUTTY": "견과류",
        "COCOA": "코코아",
        "DARK CHOCOLATE": "다크 초콜릿",
        "MILK CHOCOLATE": "밀크 초콜릿",
        "CINNAMON": "시나몬",
        "CLOVE": "정향",
        "NUTMEG": "육두구",
        "HERBAL": "허브",
        "SMOKY": "스모키",
        "TOBACCO": "담배",
        "ROASTED GRAIN": "구운 곡물",
        "MALT": "맥아",
        
        # Detail keywords (Level 3)
        "STRAWBERRY": "딸기",
        "RASPBERRY": "라즈베리",
        "BLUEBERRY": "블루베리",
        "BLACKBERRY": "블랙베리",
        "FIG": "무화과",
        "DATE": "대추야자",
        "PRUNE": "자두",
        "RAISIN": "건포도",
        "LEMON": "레몬",
        "LIME": "라임",
        "ORANGE": "오렌지",
        "GRAPEFRUIT": "자몽",
        "APPLE": "사과",
        "PEAR": "배",
        "GRAPE": "포도",
        "MELON": "멜론",
        "DARJEELING": "다즐링",
        "EARL GREY": "얼그레이",
        "CEYLON": "실론",
        "DIAN HONG": "전홍",
        "LAVENDER": "라벤더",
        "CHAMOMILE": "캐모마일",
        "HONEYSUCKLE": "인동덩굴",
        "YLANG YLANG": "일랑일랑",
        "SWEET JASMINE": "스위트 자스민",
        "ROYAL JASMINE": "로열 자스민",
        "ARABIAN JASMINE": "아라비안 자스민",
        "WINTER JASMINE": "겨울 자스민",
        "ROSE PETAL": "장미 꽃잎",
        "ROSEWATER": "로즈워터",
        "ENGLISH ROSE": "잉글리시 로즈",
        "GRANDIFLORA": "그랜디플로라",
        "CARAMEL": "캐러멜",
        "TOFFEE": "토피",
        "BROWN SUGAR": "흑설탕",
        "DALGONA": "달고나",
        "LIGHT HONEY": "연한 꿀",
        "WILDFLOWER": "야생화 꿀",
        "MANUKA": "마누카",
        "ACACIA": "아카시아",
        "DARK MOLASSES": "다크 당밀",
        "LIGHT MOLASSES": "라이트 당밀",
        "BLACKSTRAP": "블랙스트랩",
        "SORGHUM": "수수",
        "VANILLA POD": "바닐라 빈",
        "CREAMY VANILLA": "크리미 바닐라",
        "INDIAN VANILLA": "인디안 바닐라",
        "MEXICAN VANILLA": "멕시칸 바닐라",
        "PEANUT": "땅콩",
        "HAZELNUT": "헤이즐넛",
        "ALMOND": "아몬드",
        "WALNUT": "호두",
        "COCOA POWDER": "코코아 파우더",
        "CACAO NIB": "카카오 닙",
        "FORASTERO": "포라스테로",
        "CHUAO": "추아오",
        "DARK CHOCOLATE": "다크 초콜릿",
        "BITTERSWEET": "비터스위트",
        "SEMISWEET": "세미스위트",
        "BLACK COCOA": "블랙 코코아",
        "MILK CHOCOLATE": "밀크 초콜릿",
        "WHITE CHOCOLATE": "화이트 초콜릿",
        "RUBY CHOCOLATE": "루비 초콜릿",
        "CANDY MELTS": "캔디 멜츠",
        "SWEET CINNAMON": "스위트 시나몬",
        "WOODY CINNAMON": "우디 시나몬",
        "SPICY CINNAMON": "스파이시 시나몬",
        "TOASTED CINNAMON": "토스티드 시나몬",
        "SPICY CLOVE": "스파이시 정향",
        "SWEET CLOVE": "스위트 정향",
        "WOODY CLOVE": "우디 정향",
        "MEDICINAL CLOVE": "약용 정향",
        "FRESH NUTMEG": "신선한 육두구",
        "SWEET NUTMEG": "스위트 육두구",
        "WARM NUTMEG": "따뜻한 육두구",
        "WOODY NUTMEG": "우디 육두구",
        "MINT": "민트",
        "THYME": "타임",
        "SAGE": "세이지",
        "BASIL": "바질",
        "PEATY SMOKE": "피티 스모크",
        "SWEET SMOKE": "스위트 스모크",
        "CHARCOAL": "숯",
        "CAMPFIRE": "캠프파이어",
        "PIPE TOBACCO": "파이프 담배",
        "CIGAR LEAF": "시가 잎",
        "DRY CIGAR": "드라이 시가",
        "SWEET PIPE": "스위트 파이프",
        "CEREAL": "시리얼",
        "TOASTED BREAD": "토스트",
        "TOASTED BARLEY": "볶은 보리",
        "MALTED GRAIN": "맥아 곡물",
        "MALTED BARLEY": "맥아 보리",
        "MALT SYRUP": "맥아 시럽",
        "NUTTY MALT": "견과류 맥아",
        "TOFFEE MALT": "토피 맥아",
    }


def seed_vocabulary():
    """Seed vocabulary terms for nose, palate, finish based on Flavor Wheel"""
    db = SessionLocal()
    
    try:
        # Clear existing vocabulary terms for fresh start
        # Comment out if you want to keep existing data
        # db.query(VocabularyTerm).delete()
        # db.commit()
        
        # Get existing terms to avoid duplicates
        # (scope, term, level) 조합으로 체크하여 같은 term이 다른 level에 저장 가능하도록
        existing_terms = {(term.scope, term.term, term.level) for term in db.query(VocabularyTerm).all()}
        
        # Load flavor categories and translations
        flavor_data = load_flavor_categories()
        korean_translations = get_korean_translation()
        
        # Icon mapping for categories
        icon_mapping = {
            # Categories (Level 1)
            "FRUITY": "🍎",
            "FLORAL": "🌸",
            "SWEET": "🍬",
            "NUTTY": "🥜",
            "SPICY": "🌶️",
            "SAVORY": "🔥",
            # Subcategories (Level 2)
            "BERRY": "🫐",
            "DRIED FRUIT": "🍇",
            "CITRUS": "🍋",
            "OTHER FRUIT": "🍎",
            "BLACK TEA": "🍵",
            "FLORAL (GENERAL)": "🌼",
            "JASMINE": "🌺",
            "ROSE": "🌹",
            "BROWN SUGAR": "🍮",
            "HONEY": "🍯",
            "MOLASSES": "🍯",
            "VANILLA": "🌿",
            "NUTTY": "🥜",
            "COCOA": "🍫",
            "DARK CHOCOLATE": "🍫",
            "MILK CHOCOLATE": "🍫",
            "CINNAMON": "🌰",
            "CLOVE": "🌰",
            "NUTMEG": "🌰",
            "HERBAL": "🌿",
            "SMOKY": "💨",
            "TOBACCO": "🚬",
            "ROASTED GRAIN": "🌾",
            "MALT": "🌾",
            # Detail keywords (Level 3) - use subcategory icon as default
            "STRAWBERRY": "🍓",
            "RASPBERRY": "🍇",
            "BLUEBERRY": "🫐",
            "BLACKBERRY": "🫐",
            "FIG": "🫐",
            "DATE": "🍇",
            "PRUNE": "🍇",
            "RAISIN": "🍇",
            "LEMON": "🍋",
            "LIME": "🍋",
            "ORANGE": "🍊",
            "GRAPEFRUIT": "🍊",
            "APPLE": "🍎",
            "PEAR": "🍏",
            "GRAPE": "🍇",
            "MELON": "🍈",
            "PEATY SMOKE": "💨",
            "SWEET SMOKE": "💨",
            "CHARCOAL": "⚫",
            "CAMPFIRE": "🔥",
        }
        
        added_count = {"nose": 0, "palate": 0, "finish": 0}
        
        # Process each scope (nose, palate, finish)
        for scope in ["nose", "palate", "finish"]:
            # Add all flavor categories for all scopes
            for category, subcategories in flavor_data.items():
                # Level 1: Category (대분류) - 한국어로 저장
                cat_term_en = category
                cat_term_kr = korean_translations.get(cat_term_en, cat_term_en)
                
                if (scope, cat_term_kr, 1) not in existing_terms:
                    try:
                        vocab = VocabularyTerm(
                            scope=scope,
                            term=cat_term_kr,
                            icon_key=icon_mapping.get(cat_term_en, "default"),
                            category=cat_term_kr,
                            subcategory=None,
                            level=1
                        )
                        db.add(vocab)
                        db.flush()
                        existing_terms.add((scope, cat_term_kr, 1))
                        added_count[scope] += 1
                    except Exception as e:
                        db.rollback()
                        print(f"Warning: Failed to add {scope} category '{cat_term_kr}': {e}")
                        continue
                
                # Level 2 & 3: Subcategories and detail keywords
                for subcategory, detail_keywords in subcategories.items():
                    # Level 2: Subcategory (중분류) - 한국어로 저장
                    subcat_term_en = subcategory
                    subcat_term_kr = korean_translations.get(subcat_term_en, subcat_term_en)
                    
                    if (scope, subcat_term_kr, 2) not in existing_terms:
                        try:
                            vocab = VocabularyTerm(
                                scope=scope,
                                term=subcat_term_kr,
                                icon_key=icon_mapping.get(subcat_term_en, icon_mapping.get(cat_term_en, "default")),
                                category=cat_term_kr,
                                subcategory=subcat_term_kr,
                                level=2
                            )
                            db.add(vocab)
                            db.flush()
                            existing_terms.add((scope, subcat_term_kr, 2))
                            added_count[scope] += 1
                        except Exception as e:
                            db.rollback()
                            print(f"Warning: Failed to add {scope} subcategory '{subcat_term_kr}': {e}")
                            continue
                    
                    # Level 3: Detail keywords (세부 키워드) - 한국어로 저장
                    for detail_kw_en in detail_keywords:
                        detail_kw_kr = korean_translations.get(detail_kw_en, detail_kw_en)
                        
                        if (scope, detail_kw_kr, 3) not in existing_terms:
                            try:
                                # Use specific icon if available, otherwise use subcategory icon
                                icon_key = icon_mapping.get(
                                    detail_kw_en, 
                                    icon_mapping.get(subcat_term_en, icon_mapping.get(cat_term_en, "default"))
                                )
                                vocab = VocabularyTerm(
                                    scope=scope,
                                    term=detail_kw_kr,
                                    icon_key=icon_key,
                                    category=cat_term_kr,
                                    subcategory=subcat_term_kr,
                                    level=3
                                )
                                db.add(vocab)
                                db.flush()
                                existing_terms.add((scope, detail_kw_kr, 3))
                                added_count[scope] += 1
                            except Exception as e:
                                db.rollback()
                                print(f"Warning: Failed to add {scope} detail keyword '{detail_kw_kr}': {e}")
                                continue
        
        db.commit()
        print(f"Seeded vocabulary terms: {added_count['nose']} nose, {added_count['palate']} palate, {added_count['finish']} finish")
        print(f"Total: {sum(added_count.values())} terms added")
        
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

