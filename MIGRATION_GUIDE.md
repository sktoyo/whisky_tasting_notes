# 데이터베이스 초기 설정 가이드

## 개요
Flavor Wheel 기반 계층 구조 한국어 키워드 시스템으로 구성되었습니다.

## 빠른 시작 (권장)

### 원스텝 설정
```bash
python backend/reset_db.py
```

이 명령 하나로:
1. 기존 데이터베이스 삭제
2. 새 데이터베이스 생성
3. 한국어 키워드 데이터 자동 추가

### 애플리케이션 실행
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

## 수동 설정 (필요시)

### 1. 데이터베이스 삭제
```bash
# Windows
del backend\app\tasting_notes.db

# macOS/Linux
rm backend/app/tasting_notes.db
```

### 2. 새 데이터베이스 생성 및 시딩
```bash
cd backend
python -m app.seed
```

### 3. 서버 실행
```bash
uvicorn app.main:app --reload --port 8000
```

## 데이터베이스 구조

### VocabularyTerm 모델
```python
- id: 고유 ID
- scope: nose/palate/finish
- term: 키워드 (한국어)
- icon_key: 아이콘 이모지
- category: 대분류 (과일향, 꽃향, 단맛 등)
- subcategory: 중분류 (베리류, 시트러스 등)
- level: 1=대분류, 2=중분류, 3=세부키워드
```

## 키워드 시스템

### 계층적 구조 (한국어)
- **1단계 (대분류)**: 과일향, 꽃향, 단맛, 견과류, 향신료, 고소한
- **2단계 (중분류)**: 베리류, 시트러스, 바닐라, 꿀, 코코아, 시나몬 등
- **3단계 (세부 키워드)**: 딸기, 레몬, 사과, 캐러멜, 아몬드, 민트 등

### UI 동작 방식
1. **대분류 선택**: 버튼 클릭으로 카테고리 선택
2. **키워드 선택**: 표시된 세부 키워드 클릭으로 선택/해제
3. **순서 조정**: ▲/▼ 버튼으로 키워드 순서 변경
4. **커스텀 키워드**: 보라색 배경으로 구분되는 사용자 정의 키워드

## 초기 데이터 다시 만들기

언제든지 데이터베이스를 초기화하고 싶다면:
```bash
python backend/reset_db.py
```

⚠️ 주의: 모든 노트와 키워드 데이터가 삭제됩니다!

## 문제 해결

### 데이터베이스 리셋 실패
```bash
# 수동으로 삭제 후 재시도
# Windows
del backend\app\tasting_notes.db
# macOS/Linux  
rm backend/app/tasting_notes.db

# 다시 실행
python backend/reset_db.py
```

### 키워드가 표시되지 않음
1. 데이터베이스에 데이터가 있는지 확인:
```bash
cd backend
python -m app.seed
```

2. 브라우저 캐시 삭제 후 새로고침 (Ctrl+F5)
3. 브라우저 개발자 도구 콘솔에서 에러 확인

### 서버 실행 오류
```bash
# 가상환경 활성화 확인
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 의존성 설치 확인
pip install -r requirements.txt

# 서버 실행
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

