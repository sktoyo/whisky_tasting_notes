# 위스키 테이스팅 노트 MVP

로컬 환경에서 실행되는 위스키 테이스팅 노트 웹 애플리케이션입니다.

## 기능

- 테이스팅 노트 CRUD (작성/읽기/수정/삭제)
- Nose/Palate/Finish 키워드 + 상세 설명 구조
- 기본 키워드 사전 + 커스텀 키워드
- 게시판 (카드/리스트 뷰, 정렬, 검색 AND/OR)
- 오늘의 추천 노트 5건 (하루 고정 랜덤)
- Export (.txt 파일 다운로드)
- 이미지 업로드 (로컬 저장)

## 기술 스택

- Backend: FastAPI + SQLAlchemy + SQLite
- Frontend: Jinja2 SSR 템플릿 + Tailwind CSS (CDN)
- Database: SQLite

## 설치 및 실행

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

### 3. 데이터베이스 초기화 및 시드 데이터 생성

프로젝트 루트에서 실행:

```bash
cd backend
python -m app.seed
```

또는 프로젝트 루트에서:

```bash
python -m backend.app.seed
```

### 4. 서버 실행

프로젝트 루트에서 실행:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

또는 프로젝트 루트에서 직접:

```bash
python -m uvicorn app.main:app --reload --app-dir backend
```

### 5. 브라우저에서 접속

```
http://localhost:8000
```

## 프로젝트 구조

```
.
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 앱 및 라우트
│   │   ├── db.py                # 데이터베이스 설정
│   │   ├── models.py            # SQLAlchemy 모델
│   │   ├── schemas.py           # Pydantic 스키마
│   │   ├── seed.py              # 시드 데이터 스크립트
│   │   ├── services/            # 비즈니스 로직
│   │   │   ├── note_service.py
│   │   │   ├── keyword_service.py
│   │   │   └── featured_service.py
│   │   ├── templates/           # Jinja2 템플릿
│   │   │   ├── base.html
│   │   │   ├── board.html
│   │   │   ├── note_form.html
│   │   │   └── note_detail.html
│   │   ├── static/              # 정적 파일
│   │   │   └── style.css
│   │   └── uploads/             # 업로드된 이미지 (런타임 생성)
│   └── tasting_notes.db         # SQLite 데이터베이스 (자동 생성)
├── docs/
│   ├── mvp.md                   # MVP 정의
│   └── ui_spec.md               # UI 스펙
├── requirements.txt             # Python 의존성
└── README.md                    # 이 파일
```

## 주요 페이지

- `/` - 게시판 (오늘의 추천 + 노트 목록)
- `/notes/new` - 노트 작성
- `/notes/{id}` - 노트 상세
- `/notes/{id}/edit` - 노트 수정
- `/notes/{id}/export.txt` - 노트 Export

## API 엔드포인트

- `POST /api/notes` - 노트 생성
- `PUT /api/notes/{id}` - 노트 수정
- `DELETE /api/notes/{id}` - 노트 삭제
- `POST /api/keywords/custom` - 커스텀 키워드 생성

## 데이터베이스

SQLite 데이터베이스는 `backend/tasting_notes.db`에 자동 생성됩니다.

### 테이블

- `notes` - 테이스팅 노트
- `note_keywords` - 노트의 키워드 (Nose/Palate/Finish)
- `vocabulary_terms` - 기본 키워드 사전
- `user_terms` - 커스텀 키워드 후보

## 시드 데이터

기본 키워드 사전에는 각 scope(nose/palate/finish)별로 20개의 샘플 키워드가 포함되어 있습니다.

시드 데이터를 다시 생성하려면:

```bash
# 데이터베이스 삭제 후
rm backend/tasting_notes.db  # 또는 Windows: del backend\tasting_notes.db

# 시드 재실행
python -m backend.app.seed
```

## 주의사항

- 이미지는 `backend/app/uploads/` 폴더에 저장됩니다.
- 데이터베이스는 SQLite 단일 파일로 저장됩니다.
- 인증/로그인 기능은 없습니다 (MVP 단계).

## Phase 2 (향후 계획)

- PostgreSQL 도입
- Docker/docker-compose 구성
- 배포 리허설

