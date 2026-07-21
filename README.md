# 📚 가공독서회 (Gakong Reading Club)

> **Google Gemini 2.5 Flash API와 실시간 상호작용하여 세상에 존재하지 않는 창의적이고 시적인 가상 도서를 무한히 만들어내는 예술적 디지털 라이브러리 플랫폼입니다.**

---

## ✨ 핵심 기능 소개

### 1. 실시간 AI 도서 생성 및 수명 관리
- **Google Gemini API 연동**: 사용자가 장르, 분위기, 핵심 소재를 선택하면 Gemini가 실시간으로 독창적인 도서 메타 데이터(제목, 작가, 시놉시스, 한 줄 서평, 토론 질문 등)를 생성합니다.
- **도서 자동 수명 관리**: 생성된 가상 도서는 **10일 동안 일반 도서로 노출**되며, 기한 만료 후 자동으로 **아카이브 열람** 상태로 전환됩니다.
- **관리자 권한 연동**: 관리자 계정 로그인 시 도서 상세 페이지에서 삭제 버튼이 노출되어 부적절한 도서를 연쇄(Cascade) 정단 삭제할 수 있습니다.

### 2. 👑 명예의 전당 (베스트 상상 독자 리뷰)
- **아카이브 도서 게이밍(Gamification) 위젯**: 종결된 독서방의 독자참여와 상상력을 인정하는 골드 테마의 베스트 리뷰 섹션입니다.
- **순위 & 반응 바인딩**: 🥇 1위/🥈 2위 베스트 상상 뱃지, 독자의 공감 하트수, 상상 댓글 및 **AI 작가 한줄평 답글**을 시각적으로 렌더링합니다.

### 3. 📖 몰입형 문학 목차 & 서사 감정 묘사
- **누구나 쉽게 즐기는 직관적 목차**: 과도한 한자어나 학술적 용어를 배제하고, 독자가 단번에 직관적으로 이해하고 흥미를 느낄 수 있는 친근하고 따뜻한 챕터별 줄거리를 제공합니다.
- **입체적 감정 표현 기법**: 인물의 **신체적 반응**(손끝의 경련, 턱 막히는 목구멍), **내적 동요**(서늘한 죄책감, 소용돌이치는 그리움), **역동적 동사**(응시하다, 옥죄다, 짓눌리다) 묘사를 적용하여 높은 서사적 몰입감을 전달합니다.

### 4. 🔗 콘텐츠 창작 참고 출처 (References)
본 서비스의 문학 콘텐츠 렌더링 엔진 및 서사 가이드 로직은 다음 학술/전문 자료를 학습 및 참조하여 제작되었습니다:
1. **국립국어원 표준국어대사전**: [https://stdict.korean.go.kr/main/main.do](https://stdict.korean.go.kr/main/main.do) — *풍부한 문학 어휘(유영, 궤적, 섭리, 공명, 잔상, 찰나, 파문 등) 추출 및 챕터명/줄거리 구성 반영*
2. **소설 감정표현 모음 (로다의 잉여생활)**: [https://rodalife20.tistory.com/473](https://rodalife20.tistory.com/473) *(참고도서: 《인간의 130가지 감정 표현법》)* — *신체적 반응, 내적 동요, 파워 동사 기법을 통한 독자 상상 리뷰 입체감 강화*
3. **현대소설 필수 개념 정리 (국어의 시작과 끝)**: [https://goodballad.tistory.com/11739250](https://goodballad.tistory.com/11739250) — *서술과 묘사, 액자식 구성, 말하기와 보여주기, 복선과 암시, 어조(해학/냉소/반어/풍자) 서사 이론 접목*

---

## 🛠 기술 스택 (Tech Stack)

### Backend
- **Core Framework**: FastAPI (Python 3.10+)
- **Database ORM**: SQLAlchemy / SQLite & MySQL 지원
- **AI Core**: Google Gemini 2.5 Flash API (`httpx` 비동기 통신)
- **Server**: Uvicorn

### Frontend
- **HTML/CSS/JS**: Jinja2 모듈화 템플릿 (`templates/`) & Vanilla JS (`static/js/books.js`)
- **디자인 컨셉**: 다크 테마(Dark Mode), 세련된 글래스모피즘(Glassmorphism) 및 명예의 전당 골드 테마 디자인
- **온디맨드 REST API**: 모듈화된 파셜 API 호출로 초고속 렌더링 성능 확보

---

## 📁 프로젝트 폴더 구조

```text
개인 프로젝트/
├── main.py                    # FastAPI 백엔드 메인 엔드포인트 및 Gemini API 연동 코드
├── models.py                  # SQLAlchemy DB 모델 정의 (Book, User, Comment, Rating, Library)
├── database.py                # 데이터베이스 세션 연결 설정
├── auth.py                    # 사용자 토큰 및 인증 관련 헬퍼 함수
├── bug_report_history.md      # 버그 수정 및 콘텐츠 고도화 상세 기록 문서
├── templates/                 # 모듈화된 Jinja2 템플릿 폴더
│   ├── index.html             # 메인 인덱스 구조 정의
│   ├── components/            # 네비게이션, 글로벌 푸터 공통 컴포넌트
│   └── pages/                 # 도서 상세, 명예의전당, 내 서재 등 개별 페이지 마크업
├── static/
│   ├── css/styles.css         # 글로벌 CSS 스타일 및 반응형 레이아웃 디자인
│   └── js/books.js            # 도서 렌더링, 베스트상상 리뷰, 목차 생성기 통합 스크립트
├── requirements.txt           # 파이썬 의존성 패키지 목록
└── README.md                  # 본 프로젝트 설명서
```

---

## 🚀 시작하기

### 1. 환경 설정 (.env)
```env
DATABASE_URL=sqlite:///./gakongbooks.db
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

### 2. 의존성 설치 및 실행
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
실행 후 브라우저에서 `http://localhost:8000`으로 접속하여 가공독서회를 이용하실 수 있습니다.자인 컨셉**: 다크 테마(Dark Mode), 미니멀하고 서정적인 타이포그래피, 세련된 반투명 글래스모피즘(Glassmorphism) 효과
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
