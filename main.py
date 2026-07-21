import os
import json
import asyncio
import random
import secrets
import string
import smtplib
from email.mime.text import MIMEText
from typing import List, Optional
import httpx
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from sqlalchemy import func

import database
import models
import auth

# ── 공통 유틸 헬퍼 (중복 제거) ──

def format_kst_time(dt) -> str:
    """datetime -> '오전/오후 HH:MM' 문자열로 변환합니다."""
    if not dt:
        return ""
    return dt.strftime("%p %I:%M").replace("AM", "오전").replace("PM", "오후")


def parse_reactions(raw) -> dict:
    """reactions 컬럼(JSON 문자열)을 dict로 안전하게 파싱합니다."""
    try:
        return json.loads(raw) if raw else {}
    except Exception:
        return {}


def build_reply_to_info(reply_to_id: int, db: Session):
    """reply_to_id로 부모 채팅 메시지를 조회하여 {user, text} 형태로 조립합니다."""
    if not reply_to_id:
        return None
    parent = db.query(models.ChatMessage).filter(models.ChatMessage.id == reply_to_id).first()
    if not parent:
        return None
    return {"user": parent.user.nickname, "text": parent.content}


def serialize_book(b: "models.Book", db: Session) -> dict:
    """Book 모델을 프론트엔드 응답용 dict로 직렬화합니다 (tags 파싱, 남은 기한, 참여자 수 계산 포함)."""
    book_dict = b.__dict__.copy()
    book_dict["tags"] = b.tags.split(",") if b.tags else []

    if b.created_at:
        delta = models.get_kst_now() - b.created_at
        remaining = b.deadline_days - delta.days
        book_dict["deadline_days"] = max(0, remaining)
    else:
        book_dict["deadline_days"] = b.deadline_days or 10

    participant_count = db.query(func.count(func.distinct(models.ChatMessage.user_id))).filter(
        models.ChatMessage.book_id == b.id
    ).scalar()
    book_dict["participant_count"] = participant_count or 0
    return book_dict


def calc_page_count(genre: str) -> int:
    """장르에 따른 무작위 페이지 수(10단위)를 산정합니다."""
    if '추리' in genre or '스릴러' in genre:
        return random.randint(32, 42) * 10
    elif 'SF' in genre or '판타지' in genre:
        return random.randint(38, 52) * 10
    elif '에세이' in genre or '비문학' in genre:
        return random.randint(20, 26) * 10
    elif '소설' in genre or '드라마' in genre or '로맨스' in genre:
        return random.randint(28, 35) * 10
    else:
        return random.randint(28, 38) * 10


def get_owned_chat_message(chat_id: int, current_user_id: int, db: Session, action: str = "수정") -> "models.ChatMessage":
    """본인이 작성한 채팅 메시지를 조회합니다. 없거나 본인 것이 아니면 예외를 발생시킵니다."""
    msg = db.query(models.ChatMessage).filter(models.ChatMessage.id == chat_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="존재하지 않는 메시지입니다.")
    if msg.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"본인이 작성한 메시지만 {action}할 수 있습니다."
        )
    return msg


# ── 책 표지 프롬프트 생성 헬퍼 ──
def build_cover_prompt(book: dict, selected_tone: str) -> str:
    """Generate a concise, unique prompt for AI‑image generation of a book cover."""
    visual_tags = [t.lstrip('#') for t in book.get('tags', [])[:3]]
    tags_str = ', '.join(visual_tags) if visual_tags else 'abstract, imaginative'
    return (
        f"Generate a high‑resolution book cover for the novel titled \"{book.get('title', 'Untitled')}\". "
        f"by {book.get('author', 'Unknown Author')}. "
        f"Genre: {book.get('genre', 'Fiction')}, Tone: {selected_tone}. "
        f"Key visual elements: {tags_str}. "
        "Style: cinematic, vibrant colors, 2:3 aspect ratio, suitable for display on a digital library platform."
    )

# Read .env manually (uvicorn reloader 환경에서도 안정적으로 동작)
try:
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ[k] = v
except Exception:
    pass

# 1. 데이터베이스 테이블 자동 생성
# 백엔드가 구동될 때 MySQL에 필요한 모든 테이블을 자동으로 생성합니다.
models.Base.metadata.create_all(bind=database.engine)

# DB 스키마 동적 패치 (기존 DB 테이블에 immersion_data 컬럼이 없으면 추가)
try:
    from sqlalchemy import text
    with database.engine.connect() as conn:
        # books 테이블
        try:
            conn.execute(text("ALTER TABLE books ADD COLUMN immersion_data TEXT;"))
            conn.commit()
            print("[DB Patch] Added 'immersion_data' column to 'books' table.")
        except Exception:
            pass
        
        # candidate_books 테이블
        try:
            conn.execute(text("ALTER TABLE candidate_books ADD COLUMN immersion_data TEXT;"))
            conn.commit()
            print("[DB Patch] Added 'immersion_data' column to 'candidate_books' table.")
        except Exception:
            pass
except Exception as e:
    print(f"[DB Patch] Failed to alter DB: {e}")

def get_or_create_moderator(db: Session):
    moderator = db.query(models.User).filter(models.User.email == "admin@admin.com").first()
    if not moderator:
        moderator = models.User(
            email="admin@admin.com",
            nickname="🎙️ AI 사회자",
            password_hash=auth.get_password_hash("admin1234"),
            is_admin=True
        )
        db.add(moderator)
        db.commit()
        db.refresh(moderator)
    else:
        # 이미 존재하는 경우 admin 권한과 사회자 닉네임 설정 강제화
        moderator.is_admin = True
        moderator.nickname = "🎙️ AI 사회자"
        db.commit()
        db.refresh(moderator)
    return moderator

async def trigger_ai_moderator_response(book_id: int, user_message_id: int = None):
    """
    백그라운드 스레드에서 작동하여 책 정보와 최근 독자 대화를 바탕으로
    AI 사회자가 맥락에 맞춘 질문이나 멘트를 남기도록 유도합니다.
    """
    db = database.SessionLocal()
    try:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if not book or book.is_archived:
            return
            
        moderator = db.query(models.User).filter(models.User.email == "admin@admin.com").first()
        if not moderator:
            return
            
        # 최근 독자 대화 내역 가져오기 (마지막 8개)
        recent_messages = db.query(models.ChatMessage).filter(
            models.ChatMessage.book_id == book_id
        ).order_by(models.ChatMessage.id.desc()).limit(8).all()
        
        # 순서 뒤집어서 시간순 정렬
        recent_messages.reverse()
        
        # 마지막 메시지가 이미 사회자라면 연속 개입 차단 (멘션 응답인 경우는 예외로 허용)
        if not user_message_id and recent_messages and recent_messages[-1].user_id == moderator.id:
            return
            
        chat_history_str = ""
        for m in recent_messages:
            chat_history_str += f"{m.user.nickname}: {m.content}\n"
            
        # 멘션 관련 처리
        user_message = None
        if user_message_id:
            user_message = db.query(models.ChatMessage).filter(models.ChatMessage.id == user_message_id).first()

        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key or gemini_key == "YOUR_GEMINI_API_KEY_HERE":
            # Fallback 질문 선택
            if user_message:
                moderator_content = f"{user_message.user.nickname}님, 흥미로운 질문이네요! 『{book.title}』의 세계관에서는 말씀해주신 부분 외에도 다양한 해석의 갈래가 존재한답니다. 다른 독자님들은 어떻게 생각하시나요?"
            else:
                questions = book.additional_questions.split("|") if book.additional_questions else []
                if not questions:
                    questions = [book.core_dilemma] if book.core_dilemma else ["이 책의 주인공의 선택에 대해 어떻게 생각하시나요?"]
                chosen_q = random.choice(questions)
                moderator_content = f"독자님들의 흥미로운 의견 잘 듣고 있습니다. 토론을 더 깊이 이어가기 위해 질문을 드려요. {chosen_q}"
        else:
            if user_message:
                prompt = f"""
                당신은 '가공독서회(Gakong Reading Club)'의 따뜻하고 사색적인 'AI 사회자'입니다.
                독자들이 실제로 존재하지 않는 소설인 『{book.title}』(장르: {book.genre})의 시놉시스를 읽고 상상력을 더해 서로의 감상을 나누고 있습니다.
                
                [도서 정보]
                - 제목: {book.title}
                - 작가: {book.author}
                - 시놉시스: {book.synopsis}
                - 핵심 질문(딜레마): {book.core_dilemma}
                - 등장인물 설정: {book.characters}
                
                [특수 상황: 독자의 개별 질문/의견 접수]
                독자 '{user_message.user.nickname}'님이 당신(AI 사회자)에게 직접 다음과 같이 의견을 보내거나 질문을 했습니다:
                "{user_message.content}"
                
                [수행할 작업]
                위 독자의 구체적인 질문 또는 감상에 성심껏 답변하세요.
                답변 시, 이 책이 실존하는 것처럼 『{book.title}』의 플롯, 설정, 비하인드 스토리, 등장인물들의 심리를 당신이 직접 살을 붙여 상상해내어 답변해야 합니다. 매우 구체적이고 매력적인 디테일을 지어내서 대답해 주어 독자가 가상 도서 세계관에 깊이 몰입하도록 하세요.
                
                [조건]
                1. 존댓말을 사용하고, 정중하고 서정적이며 깊이 있는 사색의 어조를 유지하세요.
                2. 독자의 닉네임({user_message.user.nickname}님)을 부르며 대답을 시작하고, 질문에 직접적으로 귀를 기울여 공감하고 통찰력 있게 답해주세요.
                3. 절대 결말을 성급하게 완전히 스포일러하거나 닫아버리지 말고, 답변 끝에 상상을 자극하는 추가 질문을 덧붙이세요.
                4. 답변의 총 길이는 공백 포함 180자 이내(절대 엄수)의 한 문단으로 짧고 강렬하게 작성하세요.
                5. 마크다운 기호나 부연설명 없이 오직 사회자 답변 텍스트만 출력하세요.
                """
            else:
                prompt = f"""
                당신은 '가공독서회(Gakong Reading Club)'의 따뜻하고 사색적인 'AI 사회자'입니다.
                독자들이 실제로 존재하지 않는 소설인 『{book.title}』(장르: {book.genre})의 시놉시스를 읽고 상상력을 더해 서로의 감상을 나누고 있습니다.
                
                [도서 정보]
                - 제목: {book.title}
                - 작가: {book.author}
                - 시놉시스: {book.synopsis}
                - 핵심 질문(딜레마): {book.core_dilemma}
                - 추가 질문들: {book.additional_questions}
                
                [최근 독자 대화 내역]
                {chat_history_str}
                
                [수행할 작업]
                위의 대화 내역과 책 정보를 바탕으로, 독자들이 상상력을 더 발휘하고 토론을 이어갈 수 있도록 돕는 사회자 멘트를 작성하세요.
                
                [조건]
                1. 존댓말을 사용하고, 정중하고 서정적이며 깊이 있는 사색의 어조를 유지하세요.
                2. 최근 독자들의 대화 내용이나 닉네임을 아주 가볍게 언급하며 공감해주세요. (예: "~~님의 의견을 보니...", "~~에 대한 관점이 흥미롭네요.")
                3. 책의 줄거리나 핵심 딜레마를 활용하여 새로운 화두나 토론용 질문을 하나 던지세요.
                4. 절대 줄거리의 결말을 마음대로 완결 짓지 마세요. 독자들의 상상을 유도하는 질문이어야 합니다.
                5. 답변의 총 길이는 공백 포함 150자 이내(절대 엄수)의 한 문단으로 짧고 강렬하게 작성하세요.
                6. 마크다운 기호나 부연설명은 일절 넣지 마세요. 오직 사회자 멘트 텍스트만 출력하세요.
                """
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.8,
                    "maxOutputTokens": 250
                }
            }
            
            moderator_content = None
            try:
                async with httpx.AsyncClient() as _client:
                    response = await _client.post(url, headers=headers, json=payload, timeout=20.0)
                if response.status_code == 200:
                    result = response.json()
                    moderator_content = result['candidates'][0]['content']['parts'][0]['text'].strip()
            except Exception as e:
                print(f"Error calling Gemini in AI moderator task: {e}")
                
            if not moderator_content:
                # Fallback on failure
                if user_message:
                    moderator_content = f"{user_message.user.nickname}님, 좋은 관점입니다. 『{book.title}』의 상징적인 표현들에 대해 다들 어떻게 느끼셨나요?"
                else:
                    questions = book.additional_questions.split("|") if book.additional_questions else []
                    if not questions:
                        questions = [book.core_dilemma] if book.core_dilemma else ["이 책의 주인공의 선택에 대해 어떻게 생각하시나요?"]
                    chosen_q = random.choice(questions)
                    moderator_content = f"독자님들의 흥미로운 의견 잘 듣고 있습니다. 토론을 더 깊이 이어가기 위해 질문을 드려요. {chosen_q}"
                
        # DB 저장
        db_msg = models.ChatMessage(
            book_id=book_id,
            user_id=moderator.id,
            content=moderator_content[:250],
            reply_to_id=user_message_id  # 멘션 응답인 경우 인용 답글 설정
        )
        db.add(db_msg)
        db.commit()
        print(f"AI Moderator message posted in book {book_id}: {moderator_content}")
    except Exception as e:
        print(f"Error in trigger_ai_moderator_response background task: {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시: 실시간 아카이브 백그라운드 루프 가동
    asyncio.create_task(realtime_archive_loop())
    print("Realtime archive background loop started.")
    
    # AI 사회자 계정 자동 생성
    db = database.SessionLocal()
    try:
        get_or_create_moderator(db)
        print("AI Moderator user initialized.")
    except Exception as e:
        print(f"Error initializing AI Moderator user: {e}")
    finally:
        db.close()
        
    yield  # 앱 실행 중
    # 앱 종료 시 필요한 정리 작업이 있다면 여기에 추가

app = FastAPI(
    title="가공독서회 (Gakong) API Server",
    description="FastAPI + MySQL + WebSockets + Gemini API 기반 백엔드 서비스",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정 (프론트엔드-백엔드 교차 통신 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOW_ORIGINS", "*").split(","),  # .env의 ALLOW_ORIGINS로 제어 (예: https://yourdomain.com)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# static 및 하위 모듈 폴더 자동 생성하여 런타임 오류 원천 차단
if not os.path.exists("static"):
    os.makedirs("static")
if not os.path.exists("static/css"):
    os.makedirs("static/css")
if not os.path.exists("static/js"):
    os.makedirs("static/js")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# ── Pydantic 데이터 검증 스키마 선언 ──

class UserSignup(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="비밀번호는 최소 8자 이상이어야 합니다.")
    nickname: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    nickname: str
    email: str
    is_admin: bool


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, description="새 비밀번호는 최소 8자 이상이어야 합니다.")

class WithdrawRequest(BaseModel):
    password: str

class UserProfile(BaseModel):
    id: int
    email: str
    nickname: str
    is_admin: bool

class FindPasswordRequest(BaseModel):
    email: EmailStr

class RatingCreate(BaseModel):
    score: int = Field(..., ge=1, le=5, description="평점은 1점에서 5점 사이여야 합니다.")


# ── 기본 정적 페이지 라우팅 ──

HTML_FILE_PATH = os.path.join(os.path.dirname(__file__), "gakong_v8_standalone.html")



def _serve_standalone_html():
    """스탠드얼론 HTML 파일을 서빙하는 공통 로직 (여러 경로 별칭에서 재사용)."""
    if os.path.exists(HTML_FILE_PATH):
        return FileResponse(HTML_FILE_PATH)
    return {"message": "가공독서회 프론트엔드 파일(gakong_v8_standalone.html)을 찾을 수 없습니다."}


@app.get("/gakong_v8", include_in_schema=False)
@app.get("/standalone", include_in_schema=False)
@app.get("/gakong_v8_standalone", include_in_schema=False)
@app.get("/gakong_v8_standalone.html", include_in_schema=False)
@app.get("/static/gakong_v8_standalone.html", include_in_schema=False)
async def get_standalone_html():
    """
    가공독서회/스탠드얼론 관련 모든 경로 별칭에서 동일한 HTML 파일을 서빙합니다.
    """
    return _serve_standalone_html()


# ── 인증 및 계정 관리 APIs (Authentication) ──

INITIAL_NICKNAMES = [
    "도서관팬", "몽상독자", "구름위에서", "기억수집가", "봄날사서", "다은이좋아", "흰구름독자", "잠못드는밤", "살아있는기억", "책속의책",
    "조용한페이지", "하늘서고", "반납불가", "기억의무게", "구름너머", "새벽사서", "책먹는여우", "영원한독자", "기억보관함", "파란하늘아래",
    "낙서독서", "밑줄긋기", "도서관미아", "별자리서재", "느린독서가", "그날의책", "사서지망생", "구름카탈로그", "기억의서가", "오래된독자",
    "책갈피요정", "문장수집가", "잉크향기", "바람의문장", "밤하늘독서", "종이비행기", "글자여행자", "오후의서재", "비오는날독서", "은하수서고",
    "새벽의문맥", "마지막책장", "첫번째단어", "이야기숲", "가공의독자"
]

NICKNAMES_FILE = os.path.join(os.path.dirname(__file__), "nicknames_pool.json")

def load_nickname_pool():
    if os.path.exists(NICKNAMES_FILE):
        try:
            with open(NICKNAMES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    with open(NICKNAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(INITIAL_NICKNAMES, f, ensure_ascii=False, indent=2)
    return INITIAL_NICKNAMES

def save_nickname_pool(pool):
    with open(NICKNAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(pool, f, ensure_ascii=False, indent=2)

async def generate_new_nicknames_via_gemini() -> List[str]:
    gemini_key = os.getenv("GEMINI_API_KEY")
    prompt = """
    가공독서회(익명 독서 토론 서비스)에서 사용할 익명 한글 닉네임 30개를 생성해 주세요.
    [조건]
    1. 반드시 독서, 서재, 사서, 도서관, 책, 문장, 감상, 종이 등 '책/독서'와 깊이 관련된 아름답고 여운이 있는 명사나 표현을 사용해 주세요. (예: 은하서림, 책갈피구름, 사서의하루)
    2. 모든 닉네임은 3자에서 8자 사이의 한글이어야 하며, 띄어쓰기가 없어야 합니다.
    3. 마크다운 기호(예: ```json)나 기타 불필요한 설명글을 절대 넣지 말고, 아래 JSON 스키마 형식 그대로의 구조화된 텍스트만 출력하세요:
    
    [
      "닉네임1", "닉네임2", ... "닉네임30"
    ]
    """
    
    if gemini_key and gemini_key != "YOUR_GEMINI_API_KEY_HERE":
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=payload, timeout=20.0)
                if response.status_code == 200:
                    result = response.json()
                    raw_text = result['candidates'][0]['content']['parts'][0]['text']
                    nicks = json.loads(raw_text.strip())
                    if isinstance(nicks, list) and len(nicks) >= 15:
                        return [str(n).strip() for n in nicks if len(str(n).strip()) >= 2]
        except Exception as e:
            print(f"Gemini 닉네임 생성 중 에러: {e}")

    # Fallback 로직: 무작위 조합형 30개 한글 독서 닉네임 생성
    adjectives = [
        "사색하는", "조용한", "깨어있는", "꿈꾸는", "빛나는", "향기로운", "고독한", "포근한", "눈부신", "기억하는",
        "비밀의", "새벽의", "달빛의", "바람의", "은빛의", "숨겨진", "아름다운", "흐르는", "아늑한", "깊어가는"
    ]
    nouns = [
        "독서가", "사서", "책방", "서가", "문장", "글방", "책갈피", "종이배", "단어", "구절",
        "독자", "도서관", "서점", "펜촉", "책장", "서고", "일기장", "이야기", "낭독가", "번역가"
    ]
    
    fallback_nicks = []
    attempts = 0
    while len(fallback_nicks) < 30 and attempts < 200:
        attempts += 1
        new_nick = f"{random.choice(adjectives)}{random.choice(nouns)}"
        if new_nick not in fallback_nicks:
            fallback_nicks.append(new_nick)
    return fallback_nicks

@app.get("/api/auth/generate-nickname")
async def api_generate_unique_nickname(db: Session = Depends(database.get_db)):
    # 1. DB의 기존 가입자 닉네임 목록 가져오기
    registered_nicknames = {u.nickname for u in db.query(models.User).all()}
    
    # 2. 파일에서 현재 닉네임 풀 로드
    pool = load_nickname_pool()
    
    # 3. 등록되지 않은 가용 닉네임 필터링
    available = [n for n in pool if n not in registered_nicknames]
    
    # 4. 풀이 소진된 경우 (가용 닉네임이 없으면) 30개 추가 생성
    if not available:
        new_nicks = await generate_new_nicknames_via_gemini()
        # 중복 방지 필터링
        filtered_new_nicks = []
        for n in new_nicks:
            if n not in pool and n not in registered_nicknames and n not in filtered_new_nicks:
                filtered_new_nicks.append(n)
                
        # 만약 필터링 후에도 너무 작다면 추가 조합형 긴급 충전
        if len(filtered_new_nicks) < 10:
            fallback_list = await generate_new_nicknames_via_gemini() # will hit fallback
            for fn in fallback_list:
                if fn not in pool and fn not in registered_nicknames and fn not in filtered_new_nicks:
                    filtered_new_nicks.append(fn)
                    
        # 풀 업데이트 및 영구 저장
        pool.extend(filtered_new_nicks)
        save_nickname_pool(pool)
        
        # 가용 닉네임 갱신
        available = [n for n in filtered_new_nicks]
        
    # 가용 닉네임이 여전히 없으면(초비상 극단적 상황) 무작위 접미사 추가로 완전 차단
    if not available:
        chosen = f"가공의독서가{random.randint(100, 999)}"
    else:
        chosen = random.choice(available)
        
    return {"nickname": chosen}

@app.post("/api/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(user_data: UserSignup, db: Session = Depends(database.get_db)):
    # 1. 이메일 중복 체크
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 가입된 이메일 주소입니다."
        )
    
    # 2. 닉네임 중복 체크 (안전 가드)
    existing_nickname = db.query(models.User).filter(models.User.nickname == user_data.nickname).first()
    if existing_nickname:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 닉네임입니다. 새로고침하여 다른 닉네임을 할당받으십시오."
        )
    
    # 3. 비밀번호 암호화 및 신규 유저 인서트
    hashed_pw = auth.get_password_hash(user_data.password)
    db_user = models.User(
        email=user_data.email,
        password_hash=hashed_pw,
        nickname=user_data.nickname
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "회원가입이 완료되었습니다. 환영합니다!", "nickname": db_user.nickname}


@app.post("/api/auth/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(database.get_db)):
    # 1. 회원 정보 조회
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    if not user or not auth.verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )
    
    # 2. JWT 토큰 발행
    access_token = auth.create_access_token(data={"user_id": user.id, "email": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "nickname": user.nickname,
        "email": user.email,
        "is_admin": user.is_admin
    }


@app.get("/api/auth/me", response_model=UserProfile)
def get_my_profile(
    current_user_id: int = Depends(auth.get_current_user_id), 
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자 정보를 찾을 수 없습니다.")
    return user

@app.post("/api/auth/change-password")
def change_password(
    req: ChangePasswordRequest,
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    """
    로그인한 회원의 비밀번호를 안전하게 검증한 후 해싱하여 교체합니다.
    """
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        
    # 1. 현재 비밀번호 검증
    if not auth.verify_password(req.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="현재 비밀번호가 올바르지 않습니다.")
        
    # 2. 새 비밀번호 해싱 및 교체
    user.password_hash = auth.get_password_hash(req.new_password)
    db.commit()
    return {"message": "비밀번호가 성공적으로 변경되었습니다. 🔒"}


@app.post("/api/auth/withdraw")
def withdraw_account(
    req: WithdrawRequest,
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    """
    회원 탈퇴 및 계정 영구 삭제 (모든 서재 및 작성 댓글 연쇄 삭제)
    """
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        
    # 1. 본인 확인용 비밀번호 재검증
    if not auth.verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=400, detail="비밀번호가 올바르지 않습니다. 탈퇴 처리에 실패했습니다.")
        
    # 2. 유저 계정 삭제 (SQLAlchemy cascade 설정에 의해 외래키 데이터 일괄 연쇄 삭제)
    db.delete(user)
    db.commit()
    return {"message": "회원 탈퇴 및 계정 영구 삭제가 완료되었습니다. 그동안 이용해 주셔서 감사합니다. 🌲"}


# ── 비밀번호 분실 복구 및 구글 SMTP 발송 유틸리티 ──

def generate_temp_password(length: int = 8) -> str:
    """
    secrets 모듈을 사용해 예측 불가능한 알파벳+숫자 8자리 임시 비밀번호를 생성합니다.
    """
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def send_recovery_email(to_email: str, nickname: str, temp_pw: str):
    """
    구글 SMTP 서버를 통해 임시 비밀번호 메일을 발송합니다.
    실제 발송 주소가 플레이스홀더 상태(your_gmail_username...)면 모의 메일 전송 완료 상태로 처리하여
    에러가 터지지 않게 안전한 Fallback 처리를 내장합니다.
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    try:
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError:
        smtp_port = 587
    smtp_username = os.getenv("SMTP_USERNAME", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    smtp_from_email = os.getenv("SMTP_FROM_EMAIL", smtp_username)

    # 1. SMTP 비밀번호 미설정 시 안전 우회 (서버가 뻗는 오류 방지)
    if (
        not smtp_username 
        or not smtp_password 
        or smtp_username == "your_gmail_username@gmail.com"
        or smtp_password == "your_gmail_app_password"
    ):
        print(f"[SMTP 모의 발송] 수신인: {to_email} ({nickname} 독자님) - 발송 설정이 플레이스홀더 상태이므로 메일 본문을 터미널에 출력합니다.")
        print(f"===========================================================")
        print(f"제목: [가공독서회] 임시 비밀번호가 발급되었습니다.")
        print(f"내용: 안녕하세요, {nickname} 독자님.\n요청하신 가공독서회 임시 비밀번호는 [{temp_pw}] 입니다.\n로그인 후 비밀번호 변경을 권장합니다.")
        print(f"===========================================================")
        return

    # 2. 실제 SMTP 발송 시도
    try:
        msg = MIMEText(
            f"안녕하세요, {nickname} 독자님.\n\n"
            f"가공독서회를 사랑해 주셔서 진심으로 감사드립니다.\n"
            f"회원님의 계정 분실 방지를 위해 발급된 임시 비밀번호는 아래와 같습니다.\n\n"
            f"▶ 임시 비밀번호: {temp_pw}\n\n"
            f"로그인하신 후, '내 서재 > 프로필 편집 > 비밀번호 변경'을 통해 안전한 비밀번호로 변경하여 사용하시기 바랍니다.\n"
            f"감사합니다.\n\n"
            f"🌲 가공독서회 운영진 드림",
            "plain",
            "utf-8"
        )
        msg["Subject"] = "[가공독서회] 임시 비밀번호가 발급되었습니다."
        msg["From"] = smtp_from_email
        msg["To"] = to_email

        with smtplib.SMTP(smtp_server, smtp_port, timeout=15) as server:
            server.starttls()  # TLS 보안 활성화
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_from_email, [to_email], msg.as_string())
        print(f"[SMTP 실제 발송 완료] 수신인: {to_email} ({nickname} 독자님) - 임시 비밀번호 메일 전송 성공")
    except Exception as e:
        print(f"[SMTP 실제 발송 실패] 수신인: {to_email} - 오류 상세: {e}")


@app.post("/api/auth/find-password")
def find_password(
    req: FindPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db)
):
    """
    가입 이메일을 조회하고, 임시 비밀번호를 발급한 뒤 구글 SMTP 서버를 통해 비동기 이메일로 전송합니다.
    """
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="등록되지 않은 이메일 주소입니다. 가입 정보를 재확인해 주세요."
        )

    # 1. 임시 비밀번호 난수 생성
    temp_pw = generate_temp_password(8)

    # 2. DB 비밀번호 해시 교체 및 커밋
    user.password_hash = auth.get_password_hash(temp_pw)
    db.commit()

    # 3. 비동기 백그라운드 작업으로 이메일 발송 위임 (API 응답 지연 0초 실현)
    background_tasks.add_task(
        send_recovery_email, 
        to_email=user.email, 
        nickname=user.nickname, 
        temp_pw=temp_pw
    )

    return {"message": "임시 비밀번호가 기입하신 이메일로 전송되었습니다. ✉️\n메일함을 확인해 주세요."}



# ── 진짜 Google Gemini API 기반 가상 도서 생성 및 목록 조회 APIs ──

# 가용한 표지 컬러 목록
BOOK_COLORS = ['#7b5fb8', '#2d7a50', '#8b4f25', '#b54a6a', '#2c5f8a', '#4a7a3a', '#6a4a8a', '#a03030']

def sanitize_endorsement_attr(attr: str) -> str:
    if not attr:
        return "— 평론가 (익명)"
    attr = attr.strip()
    if attr.startswith("-") and not attr.startswith("—"):
        attr = attr.replace("-", "—", 1)
    parts = attr.split()
    keywords = ["평론가", "소설가", "시인", "작가", "비평가", "학자", "연구가", "운동가", "박사", "교수", "에세이스트", "감독", "저널리스트", "칼럼니스트", "협회"]
    matched_idx = -1
    for i, part in enumerate(parts):
        if any(kw in part for kw in keywords):
            matched_idx = i
    if matched_idx != -1:
        result = " ".join(parts[:matched_idx + 1])
        if "익명" not in result:
            result = result + " (익명)"
        return result
    if len(parts) > 2:
        result = " ".join(parts[:-1])
        if "익명" not in result:
            result = result + " (익명)"
        return result
    if attr and "익명" not in attr:
        return attr + " (익명)"
    return attr



GENRE_FALLBACKS = {
    'SF': {
        'title_templates': [
            "{abstract}을 계산하는 {concrete}의 시선",
            "마지막 {concrete}와 {abstract}의 기하학",
            "{concrete} 너머의 {abstract}"
        ],
        'synopsis_templates': [
            "인공지능과 인류의 마지막 만남을 다룬 소설. 주인공 지우는 오래된 {concrete} 속에서 인류의 {abstract}에 대한 비밀 데이터를 발견한다. 기계가 학습한 인류의 마지막 순간이 펼쳐진다.",
            "우주 탐사선이 발견한 의문의 행성. 그곳에서 발견된 거대한 {concrete}은 {abstract}의 파동을 방출하고 있었다. 대원들은 자신들의 내면을 마주하며 우주의 신비에 빠져든다."
        ],
        'endorsement_quotes': [
            "기술과 {abstract}이 교차하는 아름다운 우주적 비극. 작가는 {concrete}를 통해 SF의 정수를 보여준다.",
            "숨이 멎을 듯한 묘사. {concrete}에 담긴 인간의 {abstract}을 이렇게 깊이 있게 다룰 수 있는가."
        ],
        'endorsement_attrs': [
            "SF 평론가", "소설가"
        ],
        'publisher_reviews': [
            "이 소설은 {concrete}라는 사물을 통해 미래 인류가 마주하게 될 {abstract}의 심연을 탐색한다. 작가의 시적인 상상력이 극대화된 수작.",
            "기존 SF의 틀을 깨는 서정성. {concrete}와 {abstract}의 조화는 독자들에게 깊은 감동을 안겨줄 것이다."
        ]
    },
    '판타지': {
        'title_templates': [
            "{concrete} 상점과 {abstract}의 정원",
            "자정의 {concrete}: {abstract}을 찾는 여정",
            "{abstract}을 노래하는 {concrete}의 마법"
        ],
        'synopsis_templates': [
            "마법이 사라진 시대, 한 마을의 구석에 위치한 낡은 {concrete}에서 기이한 소리가 들려온다. 주인공 다은은 {abstract}의 세계로 들어가는 문을 열고 새로운 모험을 떠난다.",
            "영원한 겨울이 계속되는 대륙. 유일하게 얼어붙지 않은 {concrete}은 {abstract}의 열기를 품고 있다. 수호자들은 이 불꽃을 지키기 위한 마지막 전쟁을 준비한다."
        ],
        'endorsement_quotes': [
            "동화 같은 아름다움 속에 숨겨진 날카로운 성찰. {concrete}는 우리 내면의 {abstract}을 비추는 거울이다.",
            "환상적인 묘사와 철학적 깊이. {concrete}와 {abstract}의 마법 같은 조화."
        ],
        'endorsement_attrs': [
            "판타지 평론가", "동화 작가"
        ],
        'publisher_reviews': [
            "어른들을 위한 가장 서정적이고 아름다운 판타지. {concrete}를 중심으로 펼쳐지는 {abstract}의 대서사시.",
            "마법처럼 펼쳐지는 문장의 향연. {concrete}의 울림 속에서 {abstract}의 해답을 찾아가는 소설."
        ]
    },
    '일반소설': {
        'title_templates': [
            "오후 세 시의 {concrete}와 {abstract}",
            "{abstract}의 끝에서 마주한 {concrete}",
            "{concrete}를 닦는 사람의 {abstract}"
        ],
        'synopsis_templates': [
            "평범한 일상 속에서 마주하는 깊은 상실을 다룬 소설. 은퇴한 주인공은 매일 아침 {concrete}을 닦으며 지난날의 {abstract}을 되새긴다. 가슴 저미는 현대인의 초상.",
            "작은 시골 마을의 오래된 {concrete}을 둘러싼 이야기들. 주인공들은 각자의 {abstract}을 숨긴 채 한자리에 모여 조용한 기적을 만들어낸다."
        ],
        'endorsement_quotes': [
            "일상을 문학적 예술로 격상시켰다. {concrete}에 투영된 {abstract}의 서정성.",
            "묵직하고 조용한 울림. {concrete}와 {abstract}의 관계를 통해 삶을 되돌아보게 만든다."
        ],
        'endorsement_attrs': [
            "문학평론가", "소설가"
        ],
        'publisher_reviews': [
            "평범함 속에서 비범한 감동을 이끌어내는 소설. {concrete}와 {abstract}은 우리의 삶을 비추는 가장 솔직한 도구이다.",
            "인간 내면의 고독과 {abstract}을 세밀하게 포착한 수작. {concrete}의 따뜻함이 독자의 마음에 스며든다."
        ]
    },
    '에세이/비문학': {
        'title_templates': [
            "{concrete}의 기록과 {abstract}의 연습",
            "{abstract}이 필요한 날, {concrete}를 열다",
            "내 삶의 {concrete}, 내 마음의 {abstract}"
        ],
        'synopsis_templates': [
            "일상의 작은 관찰에서 시작되는 삶의 지혜. 저자는 오래된 {concrete}을 통해 {abstract}이라는 복잡한 감정을 치유하고 이해해 나가는 과정을 따뜻하게 담아냈다.",
            "세상에 상처받은 이들을 위한 에세이. 길을 잃었을 때 만나는 {concrete}처럼, 내면의 {abstract}을 되찾는 성찰의 기록."
        ],
        'endorsement_quotes': [
            "읽는 것만으로도 마음이 차분해지는 문장들. {concrete}를 보며 {abstract}을 배운다.",
            "따뜻한 위로와 지혜. 우리 곁의 {concrete}가 {abstract}의 치유법이 될 수 있음을 보여준다."
        ],
        'endorsement_attrs': [
            "에세이스트", "칼럼니스트"
        ],
        'publisher_reviews': [
            "지친 일상에 건네는 따뜻한 문장들. {concrete}에서 출발하여 {abstract}에 다다르는 사색의 즐거움.",
            "내면의 성장을 돕는 친절한 길잡이. {concrete}의 기록을 통해 독자들의 {abstract}을 어루만진다."
        ]
    },
    '드라마/로맨스': {
        'title_templates': [
            "{concrete}에 적어 내린 {abstract}의 고백",
            "{abstract}의 거리에서 만난 {concrete}",
            "{concrete}를 닮은 그대와 {abstract}의 날들"
        ],
        'synopsis_templates': [
            "두 남녀의 애틋하고 따뜻한 사랑 이야기. 주인공은 어느 날 날아온 {concrete}에 적힌 {abstract}의 흔적을 쫓다가 우연한 재회를 통해 서로의 상처를 치유해 나간다.",
            "비 내리는 계절에 어울리는 감성 로맨스. 한 번도 {abstract}을 느껴본 적 없는 남자가 {concrete}를 만드는 여자를 만나 진짜 인생의 아름다움을 마주하게 된다."
        ],
        'endorsement_quotes': [
            "가장 순수한 형태의 감정이 여기 있다. {concrete}를 매개로 한 {abstract}의 고백.",
            "가슴 아리도록 아름다운 사랑. {concrete}와 {abstract}의 로맨스."
        ],
        'endorsement_attrs': [
            "로맨스 작가", "문학평론가"
        ],
        'publisher_reviews': [
            "서로 다른 상처를 가진 이들의 연대와 사랑. {concrete}가 전하는 {abstract}의 메시지.",
            "눈물과 미소를 자아내는 아름다운 드라마. {concrete}처럼 반짝이는 {abstract}의 이야기."
        ]
    },
    '철학적 에세이': {
        'title_templates': [
            "{concrete}의 미학: {abstract}을 사유하다",
            "{abstract}을 묻는 {concrete}의 시간",
            "{concrete}와 {abstract}에 관하여"
        ],
        'synopsis_templates': [
            "인생의 본질적인 질문들에 대해 사유하는 철학 에세이. 저자는 {concrete}라는 사물이 가지는 상징을 통해 {abstract}이라는 철학적 가치를 명쾌하면서도 깊이 있게 탐구한다.",
            "현대 사회에서 잊혀 가는 {abstract}의 존재. 우리는 왜 {concrete}를 보며 삶의 의미를 깨닫는가에 대한 사색적 통찰."
        ],
        'endorsement_quotes': [
            "사색을 자극하는 날카롭고 깊이 있는 성찰. {concrete}와 {abstract}의 철학.",
            "삶의 의미를 재정의하게 만든다. {concrete}를 통한 {abstract}의 사유."
        ],
        'endorsement_attrs': [
            "철학자", "비평가"
        ],
        'publisher_reviews': [
            "독자들의 내면을 끊임없이 흔들어 놓을 사색의 책. {concrete}에서 출발해 {abstract}의 심연에 이른다.",
            "더 깊은 성찰이 필요한 시대를 위한 책. {concrete}를 통해 {abstract}을 마주하는 철학적 기쁨."
        ]
    }
}


@app.post("/api/books/candidates")
async def generate_candidates(db: Session = Depends(database.get_db)):
    """
    Google Gemini API를 호출하여 세상에 없는 독창적인 책을 실시간 생성하거나 Pool에서 가져와 3개의 후보를 반환합니다.
    """
    genres = [
        'SF', '판타지', '일반소설', '에세이/비문학', '드라마/로맨스'
    ]
    tones = [
        '몽환적이고 시적인 분위기', 
        '쓸쓸하고 깊은 애잔함이 느껴지는 톤', 
        '위트 있고 경쾌한 해학적인 톤',
        '차가운 지성과 미스터리가 공존하는 차분한 분위기', 
        '기묘하고 잔혹동화 같은 음산하고 매혹적인 톤', 
        '따뜻하고 포근하며 가슴을 울리는 위로의 분위기',
        '서스펜스가 넘치며 숨 막히게 팽팽한 톤', 
        '낭만적이고 모험심을 한껏 자극하는 정열적인 분위기', 
        '가슴 저미는 철학적 고뇌가 느껴지는 톤'
    ]
    kw_abstract = [
        '망각', '상실', '귀환', '반란', '경계', '흔적', '침묵', '회상', 
        '평행 우주', '자아의 증발', '시간의 비가역성', '속삭임', '기면증', 
        '기하학적 질서', '숨겨진 관계', '거짓 진실', '우연의 일치', '심연의 응시', 
        '잔잔한 평화', '해방', '뒤틀린 기억', '이별의 잔상', '눈부신 각성',
        '영원', '해체', '고립', '도피', '불안', '권태', '향수', '환상', 
        '무의식', '죄의식', '속죄', '갈망', '망상', '집착', '순수', '모순', 
        '파괴', '소외', '운명', '선택', '희생', '부활', '망명', '기억상실', 
        '분열', '착각', '망설임', '동경', '비극', '구원', '위선', '열정'
    ]
    kw_concrete = [
        '거울', '녹음기', '안개 낀 등대', '녹슨 열쇠', '나침반', '찻잔과 민들레',
        '시계태엽 고래', '우편함', '비 내리는 밤의 기차역', '낡은 타자기', 'LP 턴테이블',
        '비밀 지하철 노선도', '안개꽃 가득한 식물원', '하늘을 나는 도서관', '모래시계',
        '검은 고양이의 눈동자', '올빼미의 정원', '은빛 조개껍데기', '박제된 나비', '오래된 안경',
        '손때 묻은 지도', '빨간 우체통', '낡은 피아노', '가스등', '오르골', 
        '은빛 동전', '빈티지 카메라', '비밀 일기장', '자물쇠', '만년필', '흑백 사진', 
        '회중시계', '빛바랜 우표', '오래된 향수병', '흔들의자', '골동품 라디오', '유리구슬', 
        '새장', '망원경', '체스판', '오래된 엽서', '빛바랜 일기', '먼지 쌓인 축음기', 
        '푸른 깃털', '주사위', '미로', '은장도', '지구본', '해시계', '오르골 상자', '촛대'
    ]

    selected_genre = random.choice(genres)
    selected_tone = random.choice(tones)
    k1 = random.choice(kw_abstract)
    k2 = random.choice(kw_concrete)
    
    # 1. Pool에서 미선택 책 꺼내오기 (최대 2권)
    pool_books = db.query(models.CandidateBook).filter(models.CandidateBook.status == 'pool').all()
    reused_candidates = []
    if pool_books:
        sample_size = min(2, len(pool_books))
        reused_candidates = random.sample(pool_books, sample_size)
    
    needed_count = 3 - len(reused_candidates)
    
    # Gemini용 프롬프트 조립
    prompt = f"""
    당신은 가공독서회(Gakong Reading Club)를 위한 천재적이고 감각적인 가상 도서 에디터입니다.

    [생성 조건]
    - 장르: {selected_genre}
    - 분위기/어조: {selected_tone}
    - 핵심 소재 1 (추상적 테마): {k1}
    - 핵심 소재 2 (구체적 사물/현상): {k2}
    - 생성 개수: 정확히 {needed_count}권

    [⚠️ 절대 금지 사항]
    1. 실존하는 작가, 소설가, 시인 등 실제 인물의 이름을 절대 사용하지 마세요.
       - 금지 예시: 무라카미 하루키, 한강, 김영하, Haruki Murakami 등
    2. 실존하는 책 제목, 작품명을 사용하거나 변형하지 마세요.
    3. 실존 출판사, 브랜드, 기관명을 언급하지 마세요.
    4. 모든 인물(작가, 등장인물 포함)은 완전히 창작된 허구의 존재여야 합니다.

    [작가 이름 생성 기준]
    - 완전히 새롭게 창작된 가상의 이름을 사용하세요.
    - 한국 작가 예시: 박서윤, 임하진, 오채린
    - 외국 작가 예시: Elara Voss, Soren Mika, Yuki Tanabe

    [서사 및 스타일 조건]
    1. 제목은 은유와 상징이 빛나는 시적인 제목이어야 합니다. 매번 완전히 새로운 패턴을 시도하세요.
    2. 줄거리(synopsis) 작성 규칙:
       - 뻔한 클리셰나 추상적인 문구는 절대 배제하세요.
       - 반드시 [주인공 소개], [주요 등장인물], [핵심 사건 및 갈등 요약]을 포함하세요.
       - 완전히 독창적이고 기발한 상황을 매번 새롭게 지어내세요.
       - 전체 길이는 3~4문장 이내(150자 내외)로 강렬하게 작성하세요.
    3. 작가의 국적과 배경을 다양하게 설정하세요 (한국, 미국, 일본, 유럽 등).
    4. 분위기/어조({selected_tone})의 정서가 문장 전반에 짙게 베어 나오도록 조정하세요.
    5. tags는 도서의 성격을 드러내는 고유 태그 4개를 생성하세요. (외국인 작가인 경우 국적 태그 1개 포함)
    6. 매 요청마다 플롯, 캐릭터 설정, 사건 배경이 절대 중복되지 않도록 무한한 다양성을 추구하세요.
    7. characters: 주요 등장인물 1~2명만 "이름 — 한 줄 인상" 형식으로 작성하세요.
       - 이름만 있고 설명이 짧을수록 좋습니다. 나이, 직업은 생략하세요.
       - 예시: "리오 — 망원경으로만 세상을 보는 남자"
       - 조연은 이름만 있어도 됩니다. 여러 인물은 파이프(|)로 구분하세요.

    마크다운 기호나 불필요한 설명글 없이 아래 JSON 스키마 형식의 '배열(Array)'로 출력하세요. 반드시 {needed_count}개의 객체가 배열 안에 있어야 합니다:

    [
      {{
        "title": "책 제목 (시적인 표현)",
        "author": "완전히 창작된 가상의 작가 이름 (외국인 작가인 경우에도 영어/라틴 문자 대신 반드시 '하나 모리', '엘라라 보스'와 같이 한국어(한글) 음독으로만 표기하세요)",
        "synopsis": "줄거리 요약 (150자 내외)",
        "tags": ["#태그1", "#태그2", "#태그3", "#태그4"],
        "price": "₩14,000",
        "page_count": 320,
        "endorsement_quote": "가상 문학평론가의 한 줄 추천사",
        "endorsement_attr": "— 직업명만 (예: — 문학평론가)",
        "publisher_review": "출판사 리뷰 문단",
        "opening_line": "소설의 첫 문장 (따옴표 제외)",
        "memorable_quote": "가장 인상 깊은 명대사 한 줄 (따옴표 제외)",
        "core_dilemma": "핵심 토론 질문 (예: Q. 고통스러운 진실을 기억할 것인가?)",
        "additional_questions": ["추가 토론 질문 1", "추가 토론 질문 2"],
        "characters": "이름 — 한 줄 인상|이름 — 한 줄 인상",
        "immersion_data": {{
          "table_of_contents": [
            {{"chapter_number": "제 1장", "title": "1장 소제목", "pages": "9 - 58", "summary": "1장 요약 (1문장)"}},
            {{"chapter_number": "제 2장", "title": "2장 소제목", "pages": "59 - 120", "summary": "2장 요약 (1문장)"}},
            {{"chapter_number": "제 3장", "title": "3장 소제목", "pages": "121 - 198", "summary": "3장 요약 (1문장)"}},
            {{"chapter_number": "제 4장", "title": "4장 소제목", "pages": "199 - 280", "summary": "4장 요약 (1문장)"}},
            {{"chapter_number": "에필로그", "title": "에필로그 소제목", "pages": "281 - 320", "summary": "에필로그 요약 (1문장)"}}
          ]
        }}
      }}
    ]

    [주의 사항]
    - page_count와 table_of_contents의 마지막 챕터 끝 페이지(예: 320)는 완전히 일치해야 합니다.
    - table_of_contents의 챕터 개수는 4~8개 사이로 page_count 크기에 알맞게 조절하세요.
    """
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    generated_books_data = []
    
    if gemini_key and gemini_key != "YOUR_GEMINI_API_KEY_HERE" and needed_count > 0:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=payload, timeout=30.0)
                if response.status_code == 200:
                    result = response.json()
                    raw_text = result['candidates'][0]['content']['parts'][0]['text']
                    data = json.loads(raw_text.strip())
                    if isinstance(data, list):
                        generated_books_data = data
                    else:
                        generated_books_data = [data]
        except Exception as e:
            print(f"Gemini API 호출 중 오류 발생: {e}. Fallback 로직으로 전환합니다.")
            
    while len(generated_books_data) < needed_count:
        fallback_genre_data = GENRE_FALLBACKS.get(selected_genre, GENRE_FALLBACKS['철학적 에세이'])
        for _ in range(15):
            raw_title = random.choice(fallback_genre_data['title_templates'])
            chosen_title = raw_title.format(abstract=k1, concrete=k2)
            existing_book = db.query(models.CandidateBook).filter(models.CandidateBook.title == chosen_title).first()
            if not existing_book:
                break
            k1 = random.choice(kw_abstract)
            k2 = random.choice(kw_concrete)
        
        raw_synopsis = random.choice(fallback_genre_data['synopsis_templates'])
        chosen_synopsis = raw_synopsis.format(abstract=k1, concrete=k2)
        raw_quote = random.choice(fallback_genre_data['endorsement_quotes'])
        chosen_quote = raw_quote.format(abstract=k1, concrete=k2)
        chosen_attr = "— " + random.choice(fallback_genre_data['endorsement_attrs'])
        raw_review = random.choice(fallback_genre_data['publisher_reviews'])
        chosen_review = raw_review.format(abstract=k1, concrete=k2)
        
        authors_pool = [
            ("한국", f"{random.choice(['박', '김', '임', '오', '윤', '정', '류', '손'])}{random.choice(['서윤', '하진', '채린', '도현', '시온', '예솔', '민재', '지후'])}"),
            ("미국", f"{random.choice(['엘라라', '소렌', '케이든', '미라', '테오', '레나', '콜'])} {random.choice(['보스', '헤일', '핀치', '렌', '대로우', '캘럼', '메리트'])}"),
            ("일본", f"{random.choice(['유키', '하나', '켄지', '아오이', '렌', '사키'])} {random.choice(['타나베', '모리', '이시다', '쿠라타', '니시노', '후지와라'])}"),
            ("프랑스", f"{random.choice(['엘리즈', '루시앙', '카미유', '테오', '마농', '라파엘'])} {random.choice(['모렐', '가르니에', '르콩트', '포르', '르나르', '보나르'])}"),
        ]
        chosen_nation, chosen_author = random.choice(authors_pool)
        
        fallback_tags = [f"#{selected_genre.split(' ')[0]}", f"#{k1}", f"#{k2}"]
        if chosen_nation != "한국":
            fallback_tags.append(f"#{chosen_nation}")
        else:
            fallback_tags.append("#AI가공")

        # Fallback용 페이지 수 미리 결정
        fallback_pages = calc_page_count(selected_genre)

        p1 = 9
        p2 = int(fallback_pages * 0.3)
        p3 = int(fallback_pages * 0.7)
        p4 = fallback_pages

        fallback_immersion = {
            "table_of_contents": [
                {"chapter_number": "제 1장", "title": f"{k2}의 그림자", "pages": f"{p1} - {p2}", "summary": f"주인공이 일상 속에서 {k2}을(를) 매개로 기묘한 {k1}의 징후를 마주하고, 감춰진 진실을 추적하기 시작합니다."},
                {"chapter_number": "제 2장", "title": f"되돌릴 수 없는 {k1}", "pages": f"{p2+1} - {p3}", "summary": f"추적 끝에 마주한 진실은 예상보다 깊은 슬픔을 품고 있었고, {k2}에 얽힌 비밀이 한 꺼풀 벗겨지며 갈등은 깊어집니다."},
                {"chapter_number": "제 3장", "title": "선택의 문턱", "pages": f"{p3+1} - {p4}", "summary": f"주인공은 {k1}을(를) 영원히 묻어둘 것인지, 아니면 비극을 감수하고 세상에 알릴 것인지 인생을 건 결단을 내려야 하는 상태에 놓입니다."}
            ]
        }

        book_data = {
            "title": chosen_title,
            "author": chosen_author,
            "synopsis": chosen_synopsis,
            "tags": fallback_tags,
            "price": f"₩{random.randint(138, 168)}00",
            "page_count": fallback_pages,
            "endorsement_quote": chosen_quote,
            "endorsement_attr": chosen_attr,
            "publisher_review": chosen_review,
            "opening_line": f"그날 밤, {k2}이(가) 내는 소리만이 세상에 남아 있었다.",
            "core_dilemma": f"Q. 당신이라면 {k1}의 진실을 마주할 것인가, 아니면 영원한 평온을 선택할 것인가?",
            "additional_questions": [
                f"Q. 작가가 이 소설에서 {k2}을(를) 중요한 상징으로 설정한 이유는 무엇일까요?",
                f"Q. 주인공이 {k1}에 대한 진실을 깨닫는 순간에 느꼈을 감정은 어땠을까요?"
            ],
            "characters": "에단 — 비밀을 파헤치는 주인공|서연 — 주인공을 돕는 조력자",
            "immersion_data": fallback_immersion
        }
        generated_books_data.append(book_data)

    final_candidates = []
    
    # 재사용 후보를 pending으로 변경
    for rb in reused_candidates:
        rb.status = 'pending'
        final_candidates.append(rb)
        
    # 신규 생성 후보 저장
    for b_data in generated_books_data:
        # 장르별 페이지 수 지정 (10단위 무작위)
        b_genre = selected_genre
        if any(t in b_data.get('tags', []) for t in ['#소설', '#일반소설', '#드라마', '#판타지', '#코지 판타지', '#다크 판타지', '#도시 판타지']):
            b_genre = '소설'

        # Gemini 생성값이 있으면 우선적으로 사용
        pages = b_data.get('page_count')
        if not pages:
            pages = calc_page_count(b_genre)

        base_price = (pages * 50) + 3000
        discounted_price = int(base_price * 0.9)
        calculated_price = f'₩{discounted_price:,}'

        add_qs = b_data.get('additional_questions', [])
        additional_qs_str = "|".join(add_qs) if isinstance(add_qs, list) else str(add_qs)

        # JSON 문자열로 직렬화하여 저장
        imm_data = b_data.get('immersion_data')
        immersion_data_str = json.dumps(imm_data, ensure_ascii=False) if isinstance(imm_data, dict) else str(imm_data) if imm_data else None

        db_cand = models.CandidateBook(
            title=b_data.get('title', '무제'),
            author=b_data.get('author', '작자 미상'),
            genre=b_genre,
            synopsis=b_data.get('synopsis', ''),
            tags=",".join(b_data.get('tags', [])),
            price=calculated_price,
            page_count=pages,
            color=random.choice(BOOK_COLORS),
            endorsement_quote=b_data.get('endorsement_quote'),
            endorsement_attr=sanitize_endorsement_attr(b_data.get('endorsement_attr')),
            publisher_review=b_data.get('publisher_review'),
            opening_line=b_data.get('opening_line', ''),
            memorable_quote=b_data.get('memorable_quote', ''),
            core_dilemma=b_data.get('core_dilemma', ''),
            additional_questions=additional_qs_str,
            characters=b_data.get('characters', ''),
            immersion_data=immersion_data_str,
            status='pending'
        )
        db.add(db_cand)
        final_candidates.append(db_cand)
        
    # 모든 후보의 색상을 서로 다르게 재배정
    if len(final_candidates) <= len(BOOK_COLORS):
        chosen_colors = random.sample(BOOK_COLORS, len(final_candidates))
        for i, cand in enumerate(final_candidates):
            cand.color = chosen_colors[i]
            
    db.commit()
    for fc in final_candidates:
        db.refresh(fc)
        
    return final_candidates

@app.post("/api/books/adopt/{candidate_id}")
async def adopt_candidate(candidate_id: int, current_user_id: int = Depends(auth.get_current_user_id), db: Session = Depends(database.get_db)):
    # 채택할 후보 도서 조회
    candidate = db.query(models.CandidateBook).filter(models.CandidateBook.id == candidate_id, models.CandidateBook.status == 'pending').first()
    if not candidate:
        raise HTTPException(status_code=404, detail="해당 후보 책을 찾을 수 없거나 이미 채택되었습니다.")

    # 정식 도서(Book)로 복사 생성
    new_book = models.Book(
        title=candidate.title,
        author=candidate.author,
        genre=candidate.genre,
        synopsis=candidate.synopsis,
        tags=candidate.tags,
        price=candidate.price,
        page_count=candidate.page_count,
        color=candidate.color,
        endorsement_quote=candidate.endorsement_quote,
        endorsement_attr=candidate.endorsement_attr,
        publisher_review=candidate.publisher_review,
        opening_line=candidate.opening_line,
        memorable_quote=candidate.memorable_quote,
        core_dilemma=candidate.core_dilemma,
        additional_questions=candidate.additional_questions,
        characters=candidate.characters,
        immersion_data=candidate.immersion_data,
        deadline_days=10,
        is_archived=False
    )
    db.add(new_book)
    
    # 상태 업데이트: 선택된 애는 adopted, 나머지 pending 상태인 것들(이전 호출의 찌꺼기들 포함)은 pool로 전환
    # (여기서는 가장 안전하게 현재 선택된 것 외의 모든 pending을 pool로 바꿔줍니다)
    candidate.status = 'adopted'
    db.query(models.CandidateBook).filter(models.CandidateBook.status == 'pending').update({"status": "pool"})
    
    db.commit()
    db.refresh(new_book)
    return new_book



def _auto_archive_expired_books(db: Session):
    """
    책의 생성일과 각 책에 설정된 deadline_days를 기준으로 기한이 만료된 독서방을 자동으로 아카이브 처리합니다.
    이때 해당 독서방의 활성 채팅(chat_messages)을 보관용 창고(past_chat_messages)로 안전하게 이전하고 기존 채팅을 삭제합니다.
    """
    active_books = db.query(models.Book).filter(models.Book.is_archived == False).all()
    expired_count = 0
    now = models.get_kst_now()
    for book in active_books:
        if book.created_at:
            deadline = book.deadline_days or 10
            cutoff = now - timedelta(days=deadline)
            if book.created_at <= cutoff:
                # 1. 책을 아카이브(종료) 상태로 변경
                book.is_archived = True
                
                # 2. 해당 책의 활성 채팅 메시지를 조회하여 보관용 테이블로 이전(Migration)
                chats = db.query(models.ChatMessage).filter(models.ChatMessage.book_id == book.id).all()
                for chat in chats:
                    # 답글 대상(부모 메시지) 정보가 있다면 역추적하여 닉네임과 본문 확보
                    reply_user = None
                    reply_content = None
                    if chat.reply_to_id:
                        parent = db.query(models.ChatMessage).filter(models.ChatMessage.id == chat.reply_to_id).first()
                        if parent:
                            reply_user = parent.user.nickname
                            reply_content = parent.content
                            
                    past_chat = models.PastChatMessage(
                        book_id=chat.book_id,
                        user_id=chat.user_id,
                        user_nickname=chat.user.nickname,
                        content=chat.content,
                        reply_to_id=chat.reply_to_id,
                        reply_to_user=reply_user,
                        reply_to_content=reply_content,
                        reactions=chat.reactions,
                        original_created_at=chat.created_at,
                        archived_at=now
                    )
                    db.add(past_chat)
                
                # 3. 보관용 창고로 이전이 완료된 기존 활성 채팅 메시지는 삭제
                if chats:
                    db.query(models.ChatMessage).filter(models.ChatMessage.book_id == book.id).delete()
                    
                expired_count += 1
                
    if expired_count > 0:
        db.commit()
    return expired_count


@app.post("/api/books/auto-archive")
def trigger_auto_archive(db: Session = Depends(database.get_db)):
    """
    만료된 독서방(생성 후 10일 경과)을 수동으로 아카이브 처리합니다.
    """
    count = _auto_archive_expired_books(db)
    return {"archived_count": count, "message": f"{count}개의 독서방이 아카이브 처리되었습니다."}


@app.get("/api/books")
def list_books(genre: Optional[str] = None, db: Session = Depends(database.get_db)):
    """
    장르별(전체/특정장르) 활성화된 도서 목록을 반환합니다.
    아카이브는 1분 루프(realtime_archive_loop)에서 자동 처리되므로 여기서는 조회만 합니다.
    """

    query = db.query(models.Book).filter(models.Book.is_archived == False)
    if genre and genre != "전체" and genre != "아카이브":
        query = query.filter(models.Book.genre == genre)
    
    books = query.order_by(models.Book.id.desc()).all()

    # 태그 쉼표 문자열을 배열로 파싱하여 응답
    return [serialize_book(b, db) for b in books]


@app.get("/api/books/archived")
def list_archived_books(db: Session = Depends(database.get_db)):
    """
    종료되어 아카이브된 책들의 리스트를 반환합니다.
    """
    books = db.query(models.Book).filter(models.Book.is_archived == True).order_by(models.Book.id.desc()).all()
    return [serialize_book(b, db) for b in books]


@app.get("/api/books/{book_id}")
def get_book_details(book_id: int, db: Session = Depends(database.get_db)):
    """
    특정 가상 도서의 상세 메타데이터와 별점 통계, 등록된 모든 감상평 목록을 로드합니다.
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="도서 정보를 찾을 수 없습니다.")
        
    # 별점 평균 통계 계산
    ratings = db.query(models.Rating).filter(models.Rating.book_id == book_id).all()
    total_ratings = len(ratings)
    avg_score = sum([r.score for r in ratings]) / total_ratings if total_ratings > 0 else 0
    rating_distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for r in ratings:
        rating_distribution[r.score] += 1

    book_dict = serialize_book(book, db)

    return {
        "book": book_dict,
        "ratings_summary": {
            "avg_score": round(avg_score, 1),
            "total_count": total_ratings,
            "distribution": rating_distribution
        }
    }


# ── 평점 관리 APIs ──


@app.post("/api/books/{book_id}/rate")
def rate_book(
    book_id: int,
    rating_data: RatingCreate,
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    """
    참여한 도서방에 1~5점 사이의 평점을 등록하거나 수정합니다.
    """
    # 도서 확인
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="존재하지 않는 독서방입니다.")
    if book.is_archived:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="종료되어 아카이브된 독서방에는 평점을 등록하거나 변경할 수 없습니다."
        )
        
    # 기존 등록 평점 확인
    existing_rating = db.query(models.Rating).filter(
        models.Rating.book_id == book_id,
        models.Rating.user_id == current_user_id
    ).first()
    
    if existing_rating:
        existing_rating.score = rating_data.score
        db.commit()
        return {"message": "평점이 성공적으로 수정되었습니다."}
    
    db_rating = models.Rating(
        book_id=book_id,
        user_id=current_user_id,
        score=rating_data.score
    )
    db.add(db_rating)
    db.commit()
    return {"message": "평점이 등록되었습니다."}


@app.delete("/api/books/{book_id}/rate")
def delete_rating(
    book_id: int,
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    """
    등록한 평점을 취소()삭제)합니다.
    """
    existing_rating = db.query(models.Rating).filter(
        models.Rating.book_id == book_id,
        models.Rating.user_id == current_user_id
    ).first()
    if not existing_rating:
        raise HTTPException(status_code=404, detail="등록된 평점이 없습니다.")
    db.delete(existing_rating)
    db.commit()
    return {"message": "평점이 취소되었습니다."}


@app.delete("/api/books/{book_id}")
def delete_book(
    book_id: int,
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    """
    도서 및 독서방을 영구 삭제합니다. (관리자 전용)
    """
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if not user or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="도서 삭제 권한이 없습니다. 관리자만 삭제할 수 있습니다."
        )
        
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="해당 도서를 찾을 수 없습니다.")
        
    db.delete(book)
    db.commit()
    return {"message": "도서가 성공적으로 삭제되었습니다."}


# ── 내 서재 담기(Library) 관리 APIs ──

@app.post("/api/library/add/{book_id}")
def add_to_library(
    book_id: int,
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    existing = db.query(models.Library).filter(
        models.Library.user_id == current_user_id,
        models.Library.book_id == book_id
    ).first()
    if existing:
        return {"message": "이미 서재에 담겨 있습니다."}
        
    db_entry = models.Library(user_id=current_user_id, book_id=book_id)
    db.add(db_entry)
    db.commit()
    return {"message": "내 서재에 책을 담았습니다. 📚"}


@app.post("/api/library/remove/{book_id}")
def remove_from_library(
    book_id: int,
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    entry = db.query(models.Library).filter(
        models.Library.user_id == current_user_id,
        models.Library.book_id == book_id
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="서재에 저장되지 않은 책입니다.")
        
    db.delete(entry)
    db.commit()
    return {"message": "내 서재에서 제외했습니다."}


@app.get("/api/library")
def get_library_books(
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    """
    유저가 서재에 담아놓은 책들과 댓글/채팅으로 참여한 책들 및 
    그에 작성한 감상(댓글/채팅) 기록집을 모두 로드합니다.
    """
    # 1. 서재에 직접 담아둔 책 ID 조회
    library_entries = db.query(models.Library).filter(models.Library.user_id == current_user_id).all()
    saved_book_ids = {entry.book_id for entry in library_entries}
    
    # 2. 내가 채팅으로 참여한 책 ID 조회
    chat_book_ids = {ch.book_id for ch in db.query(models.ChatMessage).filter(models.ChatMessage.user_id == current_user_id).all()}
    
    # 담았거나 참여한 모든 책 ID의 합집합 생성 (중복 제거)
    all_book_ids = saved_book_ids.union(chat_book_ids)
    
    saved_books = []
    
    for bid in all_book_ids:
        b = db.query(models.Book).filter(models.Book.id == bid).first()
        if not b:
            continue
            
        # 내가 작성한 채팅 추출
        my_chats = db.query(models.ChatMessage).filter(
            models.ChatMessage.book_id == b.id,
            models.ChatMessage.user_id == current_user_id
        ).all()
        
        writings = []
        for ch in my_chats:
            writings.append({
                "type": "chat",
                "text": ch.content,
                "date": ch.created_at.strftime("%Y-%m-%d %H:%M")
            })
            
        saved_books.append({
            "id": b.id,
            "title": b.title,
            "genre": b.genre,
            "author": b.author,
            "color": b.color,
            "tags": b.tags.split(",") if b.tags else [],
            "writings": writings,
            "is_saved": bid in saved_book_ids
        })
    return saved_books


# ── HTTP REST API 기반 독서방 대화(댓글 형식) 시스템 ──

class ChatCreate(BaseModel):
    text: str = Field(..., max_length=140, description="대화 내용은 최대 140자까지 입력 가능합니다.")
    reply_to_id: Optional[int] = Field(None, description="답글을 남길 대상 대화 ID")

class ReactRequest(BaseModel):
    emoji: str = Field(..., description="반응 이모지 (❤️, 🤔, 😄, ✨ 중 하나)")


@app.get("/api/books/{book_id}/chats")
def get_chat_history(book_id: int, db: Session = Depends(database.get_db)):
    """
    해당 독서방의 모든 대화 기록(댓글 리스트)을 시간순으로 조회합니다.
    """
    messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.book_id == book_id
    ).order_by(models.ChatMessage.id.asc()).all()
    
    history = []
    for m in messages:
        history.append({
            "id": m.id,
            "userId": m.user_id,
            "user": m.user.nickname,
            "text": m.content,
            "ts": format_kst_time(m.created_at),
            "date": m.created_at.isoformat(),
            "replyTo": build_reply_to_info(m.reply_to_id, db),
            "reactions": parse_reactions(m.reactions)
        })
    return history


@app.post("/api/books/{book_id}/chats")
def send_chat_message(
    book_id: int,
    chat_data: ChatCreate,
    background_tasks: BackgroundTasks,
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    """
    독서방에 한 마디 대화(댓글)를 등록합니다. (인증 필요)
    """
    # 1. 독서방 존재 유무 확인
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="존재하지 않는 독서방입니다.")
    if book.is_archived:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="종료되어 아카이브된 독서방에는 채팅을 전송할 수 없습니다."
        )
        
    # 2. 대화 메시지 DB 저장
    db_msg = models.ChatMessage(
        book_id=book_id,
        user_id=current_user_id,
        content=chat_data.text.strip(),
        reply_to_id=chat_data.reply_to_id
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    # ── AI 사회자 트리거 조건 검사 ──
    moderator = db.query(models.User).filter(models.User.email == "admin@admin.com").first()
    
    # 메시지에 @사회자 또는 @moderator가 있는지 확인
    is_mention = "@사회자" in db_msg.content or "@moderator" in db_msg.content.lower()
    
    should_trigger_moderator = False
    if moderator:
        if is_mention:
            # 멘션이 포함된 경우 즉시 백그라운드 태스크로 멘션 답변 처리 등록
            background_tasks.add_task(trigger_ai_moderator_response, book_id, db_msg.id)
        else:
            # 마지막 AI 사회자의 메시지 ID
            last_mod_msg = db.query(models.ChatMessage).filter(
                models.ChatMessage.book_id == book_id,
                models.ChatMessage.user_id == moderator.id
            ).order_by(models.ChatMessage.id.desc()).first()
            
            if not last_mod_msg:
                # AI 사회자가 아직 이 방에 글을 남기지 않았다면, 첫 번째 사용자의 메시지가 등록될 때 환영 인사 + 첫 화두 질문을 던집니다.
                should_trigger_moderator = True
            else:
                # 마지막 사회자 메시지 이후로 유저들이 작성한 메시지 수 계산
                msgs_since_last_mod = db.query(func.count(models.ChatMessage.id)).filter(
                    models.ChatMessage.book_id == book_id,
                    models.ChatMessage.id > last_mod_msg.id
                ).scalar() or 0
                
                # 유저들의 댓글이 4개 쌓일 때마다 사회자가 개입
                if msgs_since_last_mod >= 4:
                    should_trigger_moderator = True

            if should_trigger_moderator:
                background_tasks.add_task(trigger_ai_moderator_response, book_id, None)
    
    # 3. 부모 대화 인용 정보 조립
    return {
        "id": db_msg.id,
        "userId": current_user_id,
        "user": db_msg.user.nickname,
        "text": db_msg.content,
        "ts": format_kst_time(db_msg.created_at),
        "date": db_msg.created_at.isoformat(),
        "replyTo": build_reply_to_info(db_msg.reply_to_id, db)
    }




@app.post("/api/chats/{chat_id}/react")
def react_to_chat(
    chat_id: int,
    req: ReactRequest,
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    VALID_EMOJIS = {"❤️", "🤔", "😄", "✨"}
    if req.emoji not in VALID_EMOJIS:
        raise HTTPException(status_code=400, detail="지원하지 않는 이모지입니다. ❤️ 🤔 😄 ✨ 중 하나를 사용하세요.")

    msg = db.query(models.ChatMessage).filter(models.ChatMessage.id == chat_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="존재하지 않는 메시지입니다.")

    rx = parse_reactions(msg.reactions)
    rx[req.emoji] = rx.get(req.emoji, 0) + 1
    msg.reactions = json.dumps(rx, ensure_ascii=False)
    db.commit()

    return {"reactions": rx}


@app.get("/api/books/{book_id}/chat-history")
def get_chat_history_archive(book_id: int, db: Session = Depends(database.get_db)):
    """
    종료된 독서방의 채팅 기록을 읽기 전용으로 열람합니다.
    past_chat_messages 테이블을 우선 조회하고, 비어있으면 chat_messages에서 fallback합니다.
    (현재 규모에서는 대부분 chat_messages fallback이 동작합니다.)
    """
    # 1. past_chat_messages에서 아카이브된 기록 우선 조회
    past_msgs = db.query(models.PastChatMessage).filter(
        models.PastChatMessage.book_id == book_id
    ).order_by(models.PastChatMessage.original_created_at.asc()).all()

    if past_msgs:
        # past_chat_messages에 데이터가 있으면 그것을 반환
        history = []
        for m in past_msgs:
            # 답장 원본 정보 조립
            reply_to_info = None
            if m.reply_to_user and m.reply_to_content:
                reply_to_info = {"user": m.reply_to_user, "text": m.reply_to_content}

            history.append({
                "id": m.id,
                "user": m.user_nickname,
                "text": m.content,
                "ts": format_kst_time(m.original_created_at),
                "date": m.original_created_at.isoformat(),
                "replyTo": reply_to_info,
                "reactions": parse_reactions(m.reactions),
                "source": "past"
            })
        return history

    # 2. past_chat_messages가 비어있으면 chat_messages에서 fallback 조회
    # (데이터 규모가 커지기 전까지는 이 경로가 주로 사용됩니다)
    messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.book_id == book_id
    ).order_by(models.ChatMessage.id.asc()).all()

    history = []
    for m in messages:
        history.append({
            "id": m.id,
            "user": m.user.nickname,
            "text": m.content,
            "ts": format_kst_time(m.created_at),
            "date": m.created_at.isoformat(),
            "replyTo": build_reply_to_info(m.reply_to_id, db),
            "reactions": parse_reactions(m.reactions),
            "source": "live"
        })
    return history

@app.patch("/api/chats/{chat_id}")
def update_chat_message(
    chat_id: int,
    update_data: ChatCreate,
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    """
    자신이 작성한 채팅 메시지를 수정합니다. (인증 필요, 본인 메시지만 수정 가능)
    """
    msg = get_owned_chat_message(chat_id, current_user_id, db)
    msg.content = update_data.text.strip()
    db.commit()
    return {"message": "메시지가 수정되었습니다.", "id": chat_id, "text": msg.content}


@app.delete("/api/chats/{chat_id}")
def delete_chat_message(
    chat_id: int,
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    """
    자신이 작성한 채팅 메시지를 삭제합니다. (인증 필요, 본인 메시지만 삭제 가능)
    """
    msg = get_owned_chat_message(chat_id, current_user_id, db, action="삭제")
    db.delete(msg)
    db.commit()
    return {"message": "메시지가 삭제되었습니다."}


# --- 리얼타임(백그라운드) 아카이브 검사 루프 ---
async def realtime_archive_loop():
    while True:
        try:
            db = database.SessionLocal()
            _auto_archive_expired_books(db)
            db.close()
        except Exception as e:
            print(f"Realtime archive loop error: {e}")
        
        # 1분(60초)마다 백그라운드에서 실시간 만료 검사 수행
        await asyncio.sleep(60)
# ----------------------------------------------


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

# Trigger reload
