# 위스키 테이스팅 노트 웹 애플리케이션

Flavor Wheel 기반 계층 구조 키워드를 사용한 위스키 테이스팅 노트 작성/관리 시스템입니다.

## 주요 기능

- ✨ **계층적 키워드 시스템**: 대분류 → 중분류 → 세부 키워드 3단계 구조
- 🇰🇷 **한국어 지원**: 모든 키워드가 한국어로 표시
- 📝 **구조화된 노트 작성**: Nose, Palate, Finish 섹션별 키워드 및 총평
- 🖼️ **이미지 업로드**: 위스키 사진 첨부
- 🔍 **검색 및 필터링**: 키워드, 증류소, 이름으로 검색
- 📊 **게시판 뷰**: 카드/리스트 뷰 지원

## 빠른 시작

### 1. 가상환경 생성 및 활성화
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 초기화
```bash
python backend/reset_db.py
```

### 4. 서버 실행
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 5. 브라우저 접속
```
http://localhost:8000
```

## 프로젝트 구조

```
tasting_notes_web/
├── backend/
│   ├── app/
│   │   ├── models.py          # 데이터 모델
│   │   ├── main.py            # FastAPI 애플리케이션
│   │   ├── seed.py            # 데이터베이스 시딩
│   │   ├── db.py              # 데이터베이스 설정
│   │   ├── schemas.py         # Pydantic 스키마
│   │   ├── services/          # 비즈니스 로직
│   │   ├── templates/         # Jinja2 템플릿
│   │   ├── static/            # CSS/JS 파일
│   │   └── uploads/           # 업로드된 이미지
│   └── reset_db.py            # DB 리셋 스크립트
├── docs/
│   ├── ui_spec.md             # UI 명세서
│   └── flavor_category.json   # Flavor Wheel 데이터
├── requirements.txt
└── README.md
```

## 키워드 시스템

### 계층 구조
**1단계 (대분류)**: 과일향, 꽃향, 단맛, 견과류, 향신료, 고소한

**2단계 (중분류)**: 각 대분류별 4개
- 과일향: 베리류, 말린 과일, 시트러스, 기타 과일
- 꽃향: 홍차, 꽃향(일반), 자스민, 장미
- 단맛: 흑설탕, 꿀, 당밀, 바닐라
- 견과류: 견과류, 코코아, 다크 초콜릿, 밀크 초콜릿
- 향신료: 시나몬, 정향, 육두구, 허브
- 고소한: 스모키, 담배, 구운 곡물, 맥아

**3단계 (세부 키워드)**: 각 중분류별 4개
- 예: 베리류 → 딸기, 라즈베리, 블루베리, 블랙베리

### UI 사용법
1. 대분류 버튼 클릭
2. 표시된 세부 키워드 클릭하여 선택/해제
3. 선택된 키워드 영역에서 순서 조정(▲/▼) 및 삭제
4. 커스텀 키워드 추가 가능

## 기술 스택

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: Jinja2 Templates, Tailwind CSS
- **언어**: Python 3.8+

## 개발

### 데이터베이스 리셋
```bash
python backend/reset_db.py
```

### 데이터베이스 시딩만 실행
```bash
cd backend
python -m app.seed
```

### 개발 서버 실행
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

## 문제 해결

자세한 문제 해결 방법은 [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)를 참고하세요.

## 라이선스

MIT License
