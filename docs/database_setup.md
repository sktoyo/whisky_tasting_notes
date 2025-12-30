# 데이터베이스 설정 및 초기화

## DB 생성 위치 및 방법

### 1. DB 파일 위치
- **경로**: `backend/app/tasting_notes.db`
- **타입**: SQLite

### 2. DB 초기화 코드
- **파일**: `backend/app/db.py`
- **함수**: `init_db()`
  - `Base.metadata.create_all(bind=engine)` 호출
  - 모든 모델의 테이블 생성
  - **주의**: 기존 테이블이 있으면 스키마를 변경하지 않음 (CREATE TABLE IF NOT EXISTS 방식)

### 3. 서버 시작 시 자동 초기화
- **파일**: `backend/app/main.py`
- **함수**: `startup_event()` (76-81줄)
  ```python
  @app.on_event("startup")
  async def startup_event():
      init_db()              # 테이블 생성
      seed_vocabulary()      # 기본 키워드 추가
  ```

### 4. 기본 키워드 추가 (Seeding)
- **파일**: `backend/app/seed.py`
- **함수**: `seed_vocabulary()`
  - **Flavor Wheel 기반 계층 구조** 키워드 생성
  - **한국어 키워드**로 저장
  - 각 scope(nose/palate/finish)별로 동일한 계층 구조 적용
  - 대분류(level=1): 6개 (과일향, 꽃향, 단맛, 견과류, 향신료, 고소한)
  - 중분류(level=2): 각 대분류당 4개씩 총 24개
  - 세부 키워드(level=3): 각 중분류당 4개씩 총 96개
  - **자동 중복 체크**: (scope, term, level) 조합으로 중복 확인

## 데이터베이스 모델

### Note (테이스팅 노트)
```python
- name: 위스키 이름 (필수)
- distillery: 증류소
- age: 숙성년도
- cask_type: 캐스크 종류
- abv: 도수
- is_single_cask: 싱글 캐스크 여부
- cask_info: 캐스크 정보
- bottle_remaining: 잔여량
- bottle_opened_at: 개봉일
- nose_comment: Nose 한 줄 총평 (\n 구분)
- palate_comment: Palate 한 줄 총평 (\n 구분)
- finish_comment: Finish 한 줄 총평 (\n 구분)
- overall_comment: 전체 한 줄 총평 (\n 구분)
- score: 점수 (0-100)
- image_path: 이미지 경로
- is_draft: 임시저장 여부
- created_at: 작성일
- updated_at: 수정일
```

### VocabularyTerm (기본 키워드 사전)
```python
- scope: nose/palate/finish
- term: 키워드 텍스트 (한국어)
- icon_key: 아이콘 이모지 (이미 이모지로 저장됨)
- category: 대분류 (과일향, 꽃향, 단맛, 견과류, 향신료, 고소한)
- subcategory: 중분류 (베리류, 시트러스, 바닐라 등)
- level: 계층 레벨 (1=대분류, 2=중분류, 3=세부키워드)
- created_at: 생성일
- UniqueConstraint(scope, term, level): (scope, term, level) 조합 unique
  - 같은 term이 같은 scope에서 level이 다르면 별도 저장 가능
  - 예: "견과류" (level=1)과 "견과류" (level=2)는 별도 항목
```

### UserTerm (커스텀 키워드)
```python
- scope: nose/palate/finish
- term: 키워드 텍스트
- icon_key: 아이콘 매핑 키
- created_by: 사용자 ID (미래용)
- created_at: 생성일
```

### NoteKeyword (노트-키워드 연결)
```python
- note_id: 노트 ID (FK)
- scope: nose/palate/finish
- term: 키워드 텍스트
- icon_key: 아이콘 매핑 키
- detail_text: 레거시 필드 (사용 안 함, 항상 빈 값)
- position: 키워드 순서
- source_type: vocabulary/user (키워드 출처)
```

## 완전 재시작 방법

### 1. 서버 중지
모든 Python 프로세스 종료:
```powershell
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force
```

### 2. DB 삭제
```powershell
Remove-Item backend\app\tasting_notes.db -Force
```

### 3. 캐시 삭제 (선택사항)
```powershell
Remove-Item -Recurse -Force backend\app\__pycache__
Remove-Item -Recurse -Force backend\app\services\__pycache__
```

### 4. 서버 시작
```powershell
cd backend
python -m uvicorn app.main:app --reload
```

서버가 시작되면:
1. `init_db()`로 테이블 자동 생성
2. `seed_vocabulary()`로 기본 키워드 자동 추가

## DB 확인 도구

### check_db.py
**파일**: `backend/check_db.py`

실행:
```powershell
python backend\check_db.py
```

출력:
- 모든 테이블 스키마
- 각 테이블의 행 개수
- Nose/Palate/Finish 키워드 목록
- 중복 키워드 확인

### explore_db.py (대화형 탐색 도구)
**파일**: `backend/explore_db.py`

실행:
```powershell
python backend\explore_db.py
```

주요 기능:
- `tables` - 모든 테이블 목록 보기
- `show <table>` - 테이블 상세 정보 보기
- `search <keyword>` - 키워드 검색
- `hierarchy [scope]` - 계층 구조 키워드 보기
- `sql <query>` - SQL 쿼리 직접 실행

## 주의사항

### 스키마 변경 시
SQLAlchemy의 `create_all()`은 **기존 테이블을 변경하지 않습니다**.

스키마를 변경한 경우:
1. DB 파일 삭제 필요
2. 또는 마이그레이션 도구 사용 (Alembic 등)

### 키워드 계층 구조
- **Flavor Wheel 기반 3단계 계층 구조**
  - Level 1 (대분류): 과일향, 꽃향, 단맛, 견과류, 향신료, 고소한
  - Level 2 (중분류): 각 대분류별 4개 (예: 베리류, 시트러스, 바닐라 등)
  - Level 3 (세부 키워드): 각 중분류별 4개 (예: 딸기, 레몬, 사과 등)
- **중복 허용 규칙**
  - `UniqueConstraint('scope', 'term', 'level')` 사용
  - 같은 term이 같은 scope에서 level이 다르면 별도 저장 가능
  - 예: "견과류" (level=1, 대분류)와 "견과류" (level=2, 중분류)는 별도 항목
  - 예: "다크 초콜릿" (level=2, 중분류)와 "다크 초콜릿" (level=3, 세부 키워드)는 별도 항목
- **한국어 키워드**
  - 모든 키워드는 한국어로 저장됨
  - `docs/flavor_category.json`의 영어 키워드를 한국어로 번역하여 저장

