# docs/ui_spec.md
# UI & Feature Specification (Local-First)

본 문서는 **구현을 위한 UI/기능 단일 기준 문서**이다.
저장소/배포는 MVP 단계에서 로컬 우선이며, UI/기능 요구사항은 동일하게 유지한다.

---

## A. 테이스팅 노트 작성 페이지 (Create / Edit)

### A-1. 페이지 목적
- 위스키 1회 시음에 대한 구조화된 테이스팅 노트 작성 및 수정

---

### A-2. 레이아웃
- 좌측: 대표 이미지 업로드 영역
  - 정사각형
  - 이미지 1장
- 우측: 입력 폼
- 상단:
  - 페이지 제목 = 위스키 이름
- 제목 하단:
  - 위스키 정보 입력 폼

---

### A-3. 위스키 정보 입력 필드
- 이름 (필수)
- 증류소
- 숙성년도
- 캐스크 종류
- 도수(ABV)
- 싱글 캐스크 여부
  - true일 경우 캐스크 정보 입력
- 바틀 상태
  - 잔여량
  - 개봉일

---

### A-4. Nose / Palate / Finish 입력 구조 (공통)

#### 상단: 키워드 선택 영역
- **기본 키워드 목록 표시**
  - 기본 제공 키워드(VocabularyTerm): **Flavor Wheel 기반 키워드 계층 구조**
    - 1단계: 대분류 (Fruity, Floral, Sweet, Spicy, Savory 등)
    - 2단계: 중분류 (Citrus, Berry, Honey, Vanilla 등)
    - 3단계: 세부 키워드 (Apple, Lemon, Acacia, Cinnamon 등)
    - UI는 단계적 확장 방식
      - 대분류 선택 → 중분류 표시 → 세부 키워드 칩 표시
    - 적합한 세부 키워드를 모르겠으면 중분류 또는 대분류 키워드 선택 가능
  - 사용자 커스텀 키워드(UserTerm): 이전에 생성한 키워드도 표시
    - 기본 제공 분류에 맞춰서 추가
  - 모든 키워드는 아이콘과 함께 칩(chip) 형태로 표시
- **키워드 선택/해제**
  - 키워드 클릭 시 선택/해제 토글
  - 선택된 키워드는 배경색 변경으로 시각적 표시
  - 이벤트 위임 방식으로 동적 추가된 키워드도 클릭 가능
- **커스텀 키워드 추가**
  - `+ 커스텀 키워드` 버튼 클릭 시 모달 팝업
  - 새 키워드 입력 및 저장
  - 저장 즉시 선택 상태로 추가되고, 목록에도 추가됨

#### 중간: 선택된 키워드 관리
- **선택된 키워드 리스트 표시**
  - 회색 배경 영역에 선택된 키워드 나열
  - 각 키워드마다 아이콘 + 텍스트 표시
- **순서 변경 및 삭제**
  - ▲/▼ 버튼으로 순서 변경
  - 삭제 버튼으로 선택 해제
- **키워드별 상세 설명 제거**
  - 이전 버전의 textarea 입력 기능 제거됨
  - 키워드 선택만으로 충분
- **카드/리스트 노출**
  - position 기준 상위 3개만 사용

#### 하단: 섹션별 한 줄 총평
- **각 섹션별 독립적인 "한 줄 총평" 입력 영역**
  - Nose 한 줄 총평 (여러 줄 추가 가능)
  - Palate 한 줄 총평 (여러 줄 추가 가능)
  - Finish 한 줄 총평 (여러 줄 추가 가능)
- **UX**
  - 각 줄은 개별 텍스트 입력 필드
  - `+ 한 줄 추가` 버튼으로 새 줄 추가
  - 각 줄마다 삭제 버튼 제공
  - 전체 총평과 동일한 UI 패턴 사용
- **데이터 저장**
  - hidden textarea에 `\n`으로 구분하여 저장
  - 백엔드 필드: `nose_comment`, `palate_comment`, `finish_comment`

---

### A-5. 전체 총평 및 점수
- **한 줄 총평** (여러 줄 추가/삭제 가능)
  - Nose/Palate/Finish 섹션별 총평과 별도로 운영
  - 전체 노트에 대한 종합 의견/총평
  - 각 줄은 개별 텍스트 입력 필드
  - `+ 한 줄 추가` 버튼으로 줄 추가
  - 데이터: `overall_comment` 필드에 `\n`으로 구분하여 저장
- **점수** (0–100, 선택)
  - 숫자 입력 필드
  - 선택사항

---

### A-6. 액션 버튼
- 제출 (Submit)
※ 임시 저장 / 미리보기 기능 제거


---

## B. 테이스팅 노트 상세 페이지 (Read)

### B-1. 페이지 목적
- 작성된 테이스팅 노트를 읽기 전용으로 감상

### B-2. 구성
- 작성 페이지와 동일한 레이아웃
- 모든 입력 필드 읽기 전용
- 액션 버튼:
  - 수정 (Edit → 작성 페이지로 전환)
    - 기존 업로드 이미지 연결 유지
  - Export (.txt 파일 다운로드)

---

## C. 테이스팅 노트 게시판 페이지 (Board)

### C-1. 상단 섹션: 오늘의 리뷰 5건
- 하루 동안 고정되는 랜덤 5건 노트
- 전체 노트 수 < 5 → 있는 만큼만 표시
- 전체 노트 수 = 0 → 공란
- 카드 구성:
  - 대표 사진
  - 상위 3개 NPF 키워드
  - 총평 한 줄

---

### C-2. 메인 목록 영역

#### 뷰 모드
- 카드 뷰
- 리스트(자세히) 뷰
- NPF 키워드: Nose / Palate / Finish 각각 최대 3개씩 표시

#### 카드 구성
- 대표 사진
- NPF 키워드: Nose / Palate / Finish 각각 최대 3개씩 표시
- 총평 한 줄
- 클릭 시 테이스팅 노트 상세 페이지 이동

---

### C-3. 정렬 기능
- 기준:
  - 노트 제목
  - 작성 날짜
- 오름 / 내림 지원

---

### C-4. 검색 기능
- 검색 대상:
  - 노트 제목
  - 증류소
  - NPF 키워드
- 검색 조건:
  - AND / OR 조합
- 검색 결과 0건:
  - 빈 상태 UI 표시

---

## D. 공통 UI 상태
- 로딩 상태
- 저장 중 상태
- 에러 상태
- 빈 상태
  - 노트 없음
  - 검색 결과 없음

---

## E. 주요 UI 컴포넌트 목록
- PhotoUploader
- WhiskyInfoForm
- KeywordPicker(scope) - 기본/커스텀 키워드 표시 및 선택
- KeywordListManager(scope) - 선택된 키워드 순서 변경/삭제
- SectionSummaryEditor(scope) - 섹션별 한 줄 총평 편집 (Nose/Palate/Finish)
- OverallSummaryEditor - 전체 한 줄 총평 편집
- NotePreviewModal
- NoteActionBar
- NotesBoardToolbar
- NoteCard
- NoteListRow
- FeaturedNotesStrip

## E-2. 데이터 모델 필드 (Note)
- 위스키 정보: name, distillery, age, cask_type, abv, is_single_cask, cask_info
- 바틀 상태: bottle_remaining, bottle_opened_at
- 섹션별 총평: nose_comment, palate_comment, finish_comment
- 전체 평가: overall_comment, score
- 메타: image_path, is_draft, created_at, updated_at
- 관계: keywords (NoteKeyword 모델과 1:N 관계)

## E-3. 키워드 데이터 구조
- **VocabularyTerm** (기본 키워드 사전)
  - scope: nose/palate/finish
  - term: 키워드 텍스트
  - icon_key: 아이콘 매핑 키
  - UniqueConstraint(scope, term): 동일 scope 내에서 키워드 중복 불가
- **UserTerm** (사용자 커스텀 키워드)
  - scope, term, icon_key (VocabularyTerm과 동일 구조)
  - created_by: 사용자 ID (미래 확장용)
- **NoteKeyword** (노트에 연결된 키워드)
  - note_id, scope, term, icon_key
  - detail_text: 사용 안 함 (레거시, 항상 빈 값)
  - position: 키워드 순서
  - source_type: vocabulary/user (출처 구분)

---

## F. 로컬 저장/업로드 가정 (MVP)
- 노트/키워드/기본 사전 데이터는 로컬 저장소(SQLite 권장)에 저장
- 이미지 업로드는 로컬 디렉토리(`/uploads`)에 저장
- Phase 2에서 저장/업로드 방식을 교체할 수 있어야 함
