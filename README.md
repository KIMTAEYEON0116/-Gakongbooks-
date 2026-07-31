# 📚 가공독서회 (Gakong Reading Club)

> **Google Gemini 2.5 Flash API와 실시간 상호작용하여 세상에 존재하지 않는 창의적이고 시적인 가상 도서를 무한히 만들어내는 예술적 디지털 라이브러리 플랫폼입니다.**

---

## ✨ 핵심 기능 소개

### 1. 실시간 AI 도서 생성 및 수명 관리
- **Google Gemini API 연동**: 사용자가 장르, 분위기, 핵심 소재를 선택하면 Gemini가 실시간으로 독창적인 도서 메타 데이터(제목, 작가, 시놉시스, 한 줄 서평, 토론 질문 등)를 생성합니다.
- **후보 도서 보관함(Pool) FIFO 순차 소진**: 3권 중 선택받지 못한 2권은 DB 보관함(`pool`)에 자동 저장되며, "다음 책 생성" 시 오래 보관된 도서부터 선입선출(FIFO)로 불러와 **남는 책 없이 100% 깔끔하게 소진**합니다. (보관함에 3권 이상 축적 시 AI 생성을 생략하고 보관 도서를 즉시 반환하여 API 응답 속도 및 비용 최적화)
- **도서 자동 수명 관리**: 생성된 가상 도서는 **10일 동안 일반 도서로 노출**되며, 기한 만료 후 자동으로 **아카이브 열람** 상태로 전환됩니다.
- **관리자 권한 연동**: 관리자 계정 로그인 시 도서 상세 페이지에서 삭제 버튼이 노출되어 부적절한 도서를 연쇄(Cascade) 정단 삭제할 수 있습니다.

### 2. 🎙️ 독자 대화 우선 모드 AI 사회자 (Gemini 2.5 Flash)
- **독자 자율 대화 존중**: 4개 댓글마다 자동 개입하던 방식을 완전 차단하여 독자들 간의 자율적인 상상과 대화를 최우선 보장합니다.
- **명시적 `@사회자` 멘션 1회 응답**: 독자가 필요에 따라 `@사회자` 또는 `@moderator`를 태그했을 때만 3단계 샌드위치 공식(공감 1문장 + 비하인드 상상 1문장 + 역질문 1문장)으로 정갈하고 풍성하게 응답합니다.
- **문장 잘림 없는 완성형 텍스트**: Gemini 2.5 Flash 추론(Thinking Token ~950개) 모델 특성에 맞춰 `maxOutputTokens`를 **4096**으로 대폭 확장하고, DB `content` 컬럼을 `TEXT` 타입으로 마이그레이션하여 잘림 없는 문장을 제공합니다.

### 3. ❤️ 공식 반응 4종 통일 & 웜 엠버 답장하기 UX
- **공식 이모지 4종 통일**: 독서방 반응 데이터를 공식 4종(`❤️` 공감해요, `🤔` 생각이 달라요, `😄` 재밌어요, `✨` 인상 깊어요)으로 100% 엄격 통일하여 일관된 감정 표현 경험을 제공합니다.
- **답장하기(Reply) 버튼 가독성 극대화**: 댓글 반응 팝오버의 "답장하기" 버튼을 웜 엠버 그라데이션(`linear-gradient`), 볼드체 선명한 흰색 텍스트(`font-weight: 700`) 및 호버 Glow 효과로 전면 개선했습니다.

### 4. 🎨 글로벌 시원시원한 가독성 타이포그래피
- **마이크로 폰트 상향**: 기존 `8px`~`10px` 극소형 폰트 40여 곳 전수를 **`12px`~`13px`로 상향**하여 눈의 피로도를 최소화했습니다.
- **독서 및 댓글 본문 시원한 확대**: 도서 상세 제목(`24px`), 줄거리 본문(`15.5px`, 줄간격 `1.85`), 독서방 댓글 본문(`15.5px`) 및 버튼(`13.5px`)을 시원하게 확대하여 최상의 읽기 환경을 선사합니다.

### 5. 👑 명예의 전당 (베스트 상상 독자 리뷰)
본 서비스의 문학 콘텐츠 렌더링 엔진 및 서사 가이드 로직은 다음 학술/전문 자료를 학습 및 참조하여 제작되었습니다:
1. **국립국어원 표준국어대사전**: [https://stdict.korean.go.kr/main/main.do](https://stdict.korean.go.kr/main/main.do) — *풍부한 문학 어휘(유영, 궤적, 섭리, 공명, 잔상, 찰나, 파문 등) 추출 및 챕터명/줄거리 구성 반영*
2. **소설 감정표현 모음 (로다의 잉여생활)**: [https://rodalife20.tistory.com/473](https://rodalife20.tistory.com/473) *(참고도서: 《인간의 130가지 감정 표현법》)* — *신체적 반응, 내적 동요, 파워 동사 기법을 통한 독자 상상 리뷰 입체감 강화*
3. **현대소설 필수 개념 정리 (국어의 시작과 끝)**: [https://goodballad.tistory.com/11739250](https://goodballad.tistory.com/11739250) — *서술과 묘사, 액자식 구성, 말하기와 보여주기, 복선과 암시, 어조(해학/냉소/반어/풍자) 서사 이론 접목*
4. **글을 쉽게 쓰는 법 (3) - 소재를 찾는 5가지 방법 (Steemit)**: [https://steemit.com/kr/@nuhorizon/3-5](https://steemit.com/kr/@nuhorizon/3-5) — *독자 관심사 교집합 발상, 일상 사물 What-If 물음표 낚싯대 던지기, 완벽주의를 깬 기발하고 엉뚱한 상상력 유발 기법 접목*

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
