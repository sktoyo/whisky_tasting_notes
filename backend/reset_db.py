"""
데이터베이스를 삭제하고 새로 생성하는 스크립트
Run: python backend/reset_db.py
"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.db import init_db
from app.seed import seed_vocabulary

DB_PATH = os.path.join(os.path.dirname(__file__), "app", "tasting_notes.db")


def reset_database():
    """데이터베이스를 삭제하고 새로 생성"""
    print("=" * 60)
    print("데이터베이스 리셋")
    print("=" * 60)
    print()
    
    # Step 1: Delete existing database
    if os.path.exists(DB_PATH):
        print(f"1. 기존 데이터베이스 삭제 중...")
        print(f"   경로: {DB_PATH}")
        try:
            os.remove(DB_PATH)
            print("   ✓ 삭제 완료")
        except Exception as e:
            print(f"   ✗ 오류 발생: {e}")
            return
    else:
        print("1. 기존 데이터베이스 없음 (스킵)")
    print()
    
    # Step 2: Create new database
    print("2. 새 데이터베이스 생성 중...")
    try:
        init_db()
        print("   ✓ 생성 완료")
    except Exception as e:
        print(f"   ✗ 오류 발생: {e}")
        return
    print()
    
    # Step 3: Seed with Korean vocabulary
    print("3. 한국어 키워드 데이터 추가 중...")
    try:
        seed_vocabulary()
        print("   ✓ 완료")
    except Exception as e:
        print(f"   ✗ 오류 발생: {e}")
        return
    print()
    
    print("=" * 60)
    print("데이터베이스 리셋 완료!")
    print("=" * 60)
    print()
    print("다음 단계:")
    print("  cd backend")
    print("  uvicorn app.main:app --reload --port 8000")
    print()


if __name__ == "__main__":
    import sys
    import io
    
    # Windows 인코딩 문제 해결
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    # Check for --force flag
    force = '--force' in sys.argv or '-f' in sys.argv
    
    if not force:
        # 확인 메시지
        print("WARNING: 모든 데이터가 삭제됩니다!")
        print("자동으로 실행하려면: python backend/reset_db.py --force")
        print()
        try:
            response = input("계속하시겠습니까? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("취소되었습니다.")
                sys.exit(0)
        except (EOFError, KeyboardInterrupt):
            print("\n취소되었습니다.")
            sys.exit(0)
    
    reset_database()

