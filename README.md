# 📚 가공독서회 (Gakong Reading Club)

> **Google Gemini 2.5 Flash API와 실시간 상호작용하여 세상에 존재하지 않는 창의적이고 시적인 가상 도서를 무한히 만들어내는 예술적 디지털 라이브러리 플랫폼입니다.**

---

## ✨ 핵심 기능 소개

### 1. 실시간 AI 도서 생성 및 관리
- **Google Gemini API 연동**: 사용자가 장르, 분위기, 추상적/구체적 핵심 소재를 선택하여 도서 생성을 요청하면, Gemini가 실시간으로 독창적인 도서 메타 데이터(제목, 작가, 상세 시놉시스, 한 줄 서평, 가격, 페이지 수, 핵심 토론 질문 등)를 생성합니다.
- **도서 자동 수명 관리**: 생성된 모든 가상 도서는 등록된 날로부터 정확히 **10일 동안만 일반 도서로 노출**되며, 기한이 만료되면 자동으로 **아카이브 열람** 상태로 이동합니다.
- **관리자 전용 도서 삭제 기능**: 특정 관리자 계정으로 로그인하면 책 상세 페이지 내 장르 텍스트 옆에 **삭제 버튼**이 나타납니다. 관리자는 부적절한 도서를 실시간으로 완전히 삭제(Cascade 연쇄 삭제 지원)할 수 있습니다.

### 2. 도서 상세 몰입 기록 (Book Immersion Board)
- **AI 생성형 문학 콘텐츠 연동**: AI가 실시간으로 분석/작성한 고유 데이터를 바탕으로 상세한 도서 정보를 다각도로 제공하여 독자의 흥미와 상상력을 고취합니다.
- **상세 목차 (Table of Contents)**: 이야기의 흐름과 주요 시놉시스를 유추해볼 수 있는 챕터별 제목, 페이지 범위, 챕터 요약을 제공합니다.
- **인물 관계도 (Character Relationship Map)**: 작중 등장인물들의 프로필(성격/인상)과 더불어 인물 간의 협력(🤝), 적대(⚡), 중립(👤), 애정(💕) 등의 관계 유형 및 상세한 설정을 시각적이고 직관적인 카드로 렌더링합니다.
- **비하인드 설정 (Behind Trivia)**: 도서 집필에 얽힌 작가의 비화, 영감을 준 배경지식, 세계관 비하인드 스토리 등을 흥미로운 사실들로 나열하여 책의 몰입감을 더해줍니다.

### 3. 가상 독자의 한 줄 서평 (Endorsement)
- 책의 가치를 보증하는 전문가의 평가를 보여줍니다.
- 개인정보 보호와 익명성 정책을 준수하기 위해 **인위적인 가상 이름을 일절 배제**하고, 평론가/소설가/번역가 등 **직업명과 익명성 표시(`— 직업명 (익명)`)만 깔끔하게 표시**하여 신비롭고 공정한 평가 분위기를 형성합니다.

### 4. 독자 상호작용 및 라이브러리
- **별점 평점 및 반응 남기기**: 책에 대한 독자들의 하트(❤️), 물음표(🤔), 웃음(😄), 빛(✨) 반응 및 별점(1~5점)을 기록하고 시각적 통계를 제공합니다.
- **독자 코멘트 및 답글**: 실시간 독자 토론 및 답글(Thread) 작성 기능을 통해 서로의 도서 감상을 교환할 수 있습니다.
- **마이 라이브러리 (보관함)**: 관심 있는 도서를 보관함에 추가하고 편리하게 열람할 수 있습니다.
- **AI 사회자의 실시간 대화 참여**: 독자들이 대화를 남기면 백그라운드에서 AI 사회자가 맥락을 파악하고 토론을 이끌어가는 멘트나 질문을 비동기식으로 작성합니다.

---

## 🛠 기술 스택 (Tech Stack)

### Backend
- **Core Framework**: FastAPI (Python 3.10+)
- **Database ORM**: SQLAlchemy
- **Database**: MySQL / MariaDB (pymysql)
- **AI Core**: Google Gemini 2.5 Flash API (`httpx` 비동기 통신)
- **Server**: Uvicorn

### Frontend
- **HTML/CSS/JS**: Modular Jinja2 Templates (FastAPI 통합) & Standalone Single-Page (더블클릭 미리보기 지원)
- **디자인 컨셉**: 다크 테마(Dark Mode), 미니멀하고 서정적인 타이포그래피, 세련된 반투명 글래스모피즘(Glassmorphism) 효과
- **로직 모듈화**: `static/js/books.js`, `static/css/styles.css`

---

## 📁 프로젝트 폴더 구조

```text
개인 프로젝트/
├── main.py                    # FastAPI 백엔드 메인 엔드포인트 및 Gemini API 연동 코드
├── models.py                  # SQLAlchemy DB 모델 정의 (Book, User, Comment, Rating, Library)
├── database.py                # 데이터베이스 세션 연결 설정
├── auth.py                    # 사용자 토큰 및 인증 관련 헬퍼 함수
├── index_standalone.html      # [New] 빌드된 오프라인 화면 미리보기용 단일 HTML (더블클릭 실행 지원)
├── templates/                 # [New] 모듈화된 Jinja2 템플릿 폴더
│   ├── index.html             # 메인 인덱스 구조 정의
│   ├── components/            # 공통 컴포넌트 (네비게이션 바 등)
│   └── pages/                 # 도서 상세, 채팅방, 라이브러리 등 개별 페이지 마크업
├── static/
│   ├── css/
│   │   └── styles.css         # 글로벌 CSS 스타일 및 반응형 레이아웃 디자인 (포맷 최적화 완료)
│   └── js/
│       └── books.js           # 도서 렌더링, 코멘트/답글 달기, API 통신 통합 스크립트
├── requirements.txt           # 파이썬 의존성 패키지 목록
├── .gitignore                 # [New] Git 업로드 제외 대상 지정 파일 (.env 및 캐시 제외)
└── README.md                  # 본 프로젝트 설명서
```

---

## 🚀 시작하기

### 1. 환경 설정 (.env)
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 아래와 같이 설정합니다.
```env
DATABASE_URL=mysql+pymysql://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행 방법 (두 가지 방식 지원)

#### Option A: FastAPI 서버를 실행하여 전체 서비스 이용 (추천)
실시간 AI 도서 생성, DB 저장, AI 사회자와의 채팅 기능 등을 모두 활성화하여 완전한 서비스를 이용하는 방법입니다.
```bash
uvicorn main:app --reload
```
실행 후 브라우저에서 `http://localhost:8000`으로 접속하여 가공독서회를 이용하실 수 있습니다.

#### Option B: `index_standalone.html` 파일 더블클릭 (오프라인 미리보기)
서버를 가동하지 않고도 프론트엔드 UI 화면 디자인과 화면 전환 기능 등을 즉시 테스트하고 싶을 때 사용하는 방법입니다.
- 프로젝트 루트 폴더 안의 `index_standalone.html` 파일을 더블클릭하여 브라우저에서 즉시 열어볼 수 있습니다.
