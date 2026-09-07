import os
import io
import sys

# Windows 콘솔(cp949)은 이모지를 인코딩하지 못한다. 로그 한 줄 때문에 서버 초기화가
# 통째로 중단되는 것을 막기 위해, 표현할 수 없는 문자는 대체 문자로 출력하도록 완화한다.
# (실제로 '🎙️ AI 사회자' 닉네임을 출력하다 계정 정리 작업이 중단된 적이 있다)
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except Exception:
        pass
import json
import re
import asyncio
import random
import secrets
import string
import base64
import hashlib
import time
import urllib.parse
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

import config
import database
import models
import auth
import security

# ── 채팅 본문 이모지 제거 ──
# 이 서비스의 채팅은 본문에 이모지를 쓰지 않는다. 감정 표현은
# 메시지에 다는 '반응'(❤️ 🤔 😄 ✨)이 담당하므로, 본문에까지 이모지가
# 섞이면 톤이 흐트러진다. 프롬프트로 금지해도 모델이 어길 수 있어
# 저장 직전에 한 번 더 걸러낸다.
_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"   # 그림문자·보충 기호
    "\U0001F000-\U0001F2FF"   # 마작·카드·괄호문자
    "\u2600-\u27BF"           # 기타 기호 및 딩뱃
    "\u2B00-\u2BFF"           # 화살표 보충
    "\uFE0F"                   # 변이 선택자
    "\u200D"                   # ZWJ
    "\u20E3"                   # 키캡 결합문자(1️⃣ 등)
    "]+"
)


def strip_chat_emoji(text: str) -> str:
    """채팅 본문의 이모지를 제거하고 그 자리에 생긴 여백을 정리합니다."""
    if not text:
        return text
    out = _EMOJI_RE.sub("", text)
    out = re.sub(r"[ \t]{2,}", " ", out)          # 이모지가 빠지며 생긴 겹공백
    out = re.sub(r"[ \t]+\n", "\n", out)          # 줄 끝 공백
    out = re.sub(r"[ \t]+([.,!?])", r"\1", out)    # 문장부호 앞 공백
    return out.strip()


# ── AI 사회자(봇) 계정 상수 ──
# 여러 함수에서 참조하므로 모듈 상단에 고정해 둔다.
# 사회자는 반드시 한 명만 존재해야 하며(get_or_create_moderator),
# 이메일이 신원 판단 기준이다.
MODERATOR_EMAIL = config.ADMIN_SEED_EMAIL
MODERATOR_NICKNAME = "🎙️ AI 사회자"

# 시드(가상) 독자 계정의 이메일 도메인.
# 서비스 소개용으로 미리 채워 둔 대화의 작성자는 모두 이 도메인을 쓴다.
# 실사용자가 이 대화를 실제 사람의 감상으로 오해하지 않도록, 채팅 응답에 isSample 플래그를 실어
# 프론트가 '예시' 표시를 붙일 수 있게 한다. (실제 가입은 이 도메인으로 받지 않는다)
# 사회자 웰컴 카드(첫 인사)를 식별하는 문구.
# 생성과 탐지가 반드시 같은 문자열을 쓰도록 상수로 둔다.
WELCOME_MARKER = "독서방에 오신 것을 환영합니다"

SAMPLE_EMAIL_DOMAIN = "@gakong.com"


def is_sample_user(user) -> bool:
    """서비스 소개용 시드 독자 계정인지 판별한다. 봇(사회자)은 별도 플래그가 있으므로 제외."""
    if user is None or getattr(user, "is_bot", False):
        return False
    email = (getattr(user, "email", "") or "").lower()
    return email.endswith(SAMPLE_EMAIL_DOMAIN)

# ── 공통 유틸 헬퍼 (중복 제거) ──

def format_kst_time(dt) -> str:
    """datetime -> '오전/오후 HH:MM' 문자열로 변환합니다."""
    if not dt:
        return ""
    hour = dt.hour
    minute = dt.minute
    period = "오전" if hour < 12 else "오후"
    display_hour = hour if hour <= 12 else hour - 12
    if display_hour == 0:
        display_hour = 12
    return f"{period} {display_hour:02d}:{minute:02d}"


def _extract_central_motif(title: str, genre: str, synopsis: str) -> tuple:
    """
    도서 제목과 줄거리를 분석하여 고유하고 상징적인 시각 키워드를 추출하고 일러스트 프롬프트를 생성합니다.
    (motif_prompt, motif_key) 튜플을 반환하며, motif_key는 Pollinations AI 실패 시
    Editorial PIL 폴백 렌더러가 같은 계열의 전용 벡터 드로잉을 매칭하는 데도 재사용됩니다.
    """
    t = (title + " " + (synopsis or "")).lower()

    keywords = []
    motif_keys = []

    # 주요 상징 사물 및 주제 키워드 추출
    if "안개꽃" in t:
        keywords.append("glowing white gypsophila baby breath flowers in glass terrarium floating in space")
        motif_keys.append("gypsophila")
    if "식물" in t or "정원" in t or "뿌리" in t:
        keywords.append("single green plant with exposed roots growing from cracked stone block")
        motif_keys.append("plant")
    if "오르골" in t or "태엽" in t:
        keywords.append("vintage brass music box with exposed gear wheels and winding key")
        motif_keys.append("music_box")
    if "타자기" in t:
        keywords.append("antique mechanical typewriter with floating manuscript paper")
        motif_keys.append("typewriter")
    if "카메라" in t or "셔터" in t:
        keywords.append("vintage classic 35mm film camera with scattered polaroid photos")
        motif_keys.append("camera")
    if "미로" in t or "새들" in t:
        keywords.append("glowing white bird taking flight above a midnight hedge maze")
        motif_keys.append("maze")
    if "안경" in t or "렌즈" in t or "단안경" in t:
        if "항해" in t or "지도" in t:
            keywords.append("cracked antique brass monocular telescope resting on nautical sea map")
            motif_keys.append("monocle_map")
        else:
            keywords.append("round wire-rimmed spectacles resting on open antique book reflecting constellation stars")
            motif_keys.append("glasses")
    if "만년필" in t or "그림자" in t:
        keywords.append("classic fountain pen dripping ink into clock gear shadow")
        motif_keys.append("fountain_pen")
    if "시계" in t or "시간" in t or "해부" in t:
        keywords.append("vintage pocket watch spilling golden sand and clockwork gears")
        motif_keys.append("clock")
    if "섬" in t:
        keywords.append("small green island floating on calm ocean with everyday items")
        motif_keys.append("island")

    # 키워드가 비어있는 경우 장르 기반 자동 추출
    if not keywords:
        if "SF" in genre or "우주" in t:
            keywords.append("futuristic glowing holographic orb with sleek mechanical parts")
            motif_keys.append("scifi_orb")
        elif "판타지" in genre or "마법" in t:
            keywords.append("mystical enchanted spellbook with floating crystals")
            motif_keys.append("fantasy_spellbook")
        elif "로맨스" in genre or "꽃" in t:
            keywords.append("single blooming rose in clear glass vase with soft warm candlelight")
            motif_keys.append("romance_rose")
        elif "미스터리" in genre or "추리" in t:
            keywords.append("antique brass magnifying glass over scattered secret documents")
            motif_keys.append("mystery_magnifier")
        else:
            keywords.append("meaningful symbolic object casting dramatic shadow")
            motif_keys.append("generic")

    bg_style = "dark dramatic background, volumetric ethereal light" if any(k in t for k in ["우주", "밤", "자정", "어둠", "그림자", "sf"]) else "clean off-white minimalist background, soft shadows"

    motif_prompt = f"{keywords[0]}, {bg_style}"
    motif_key = motif_keys[0]
    print(f"[Keyword Extractor] 추출 키워드: '{keywords[0]}' (모티프={motif_key}, 장르={genre})")
    return motif_prompt, motif_key


def _generate_editorial_cover_pil(title: str, genre: str, synopsis: str, color: str, filepath: str, unique_id: str = "", motif_key: str = "") -> bool:
    """
    AI API 사용 불가 시 clean 바탕에 도서 고유의 상징 사물 백터 드로잉을 100% 중복 없이 생성합니다.
    motif_key(_extract_central_motif가 추출한 모티프)가 있으면 제목이 기존 시드 도서와 정확히
    일치하지 않는 신규 AI 생성 도서에도 같은 계열의 전용 렌더러가 매칭되도록 함께 판별합니다.
    """
    try:
        from PIL import Image, ImageDraw
        W, H = 450, 600
        rng = random.Random(title + str(unique_id) + color)

        t = (title + " " + (synopsis or "")).lower()

        if motif_key == "gypsophila" or "안개꽃" in title or ("안개꽃" in t and "유영" in t):
            bg = '#0F121C'
            img = Image.new('RGB', (W, H), bg)
            draw = ImageDraw.Draw(img)
            cx, cy = W // 2, H // 2 - 20
            draw.ellipse([cx - 90, cy - 90, cx + 90, cy + 90], outline='#5E81AC', width=3, fill='#151A28')
            draw.ellipse([cx - 75, cy - 75, cx + 75, cy + 75], fill='#1E2638')
            for _ in range(22):
                fx = cx + rng.randint(-55, 55)
                fy = cy + rng.randint(-55, 55)
                draw.ellipse([fx-4, fy-4, fx+4, fy+4], fill='#ECEFF4')
                draw.line([(cx, cy + 60), (fx, fy)], fill='#88C0D0', width=1)
                
        elif motif_key == "music_box" or "오르골" in title:
            bg = '#1C1612'
            img = Image.new('RGB', (W, H), bg)
            draw = ImageDraw.Draw(img)
            cx, cy = W // 2, H // 2 - 20
            draw.rounded_rectangle([cx - 80, cy - 50, cx + 80, cy + 50], radius=10, fill='#3B2D22', outline='#D08770', width=4)
            draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], outline='#EBCB8B', width=4)
            draw.ellipse([cx + 50, cy - 70, cx + 70, cy - 50], outline='#EBCB8B', width=3)
            
        elif motif_key == "typewriter" or "타자기" in title:
            bg = '#141A1D'
            img = Image.new('RGB', (W, H), bg)
            draw = ImageDraw.Draw(img)
            cx, cy = W // 2, H // 2 - 20
            draw.polygon([(cx - 80, cy + 50), (cx + 80, cy + 50), (cx + 60, cy - 10), (cx - 60, cy - 10)], fill='#2E3440', outline='#88C0D0', width=3)
            draw.rectangle([cx - 45, cy - 90, cx + 45, cy - 10], fill='#ECEFF4', outline='#4C566A')
            for row in range(3):
                for col in range(7):
                    kx = cx - 50 + col * 16
                    ky = cy + 10 + row * 12
                    draw.ellipse([kx-4, ky-4, kx+4, ky+4], fill='#81A1C1')
                    
        elif motif_key == "camera" or "셔터" in title or "카메라" in title:
            bg = '#F5F0EB'
            img = Image.new('RGB', (W, H), bg)
            draw = ImageDraw.Draw(img)
            cx, cy = W // 2, H // 2 - 20
            draw.rounded_rectangle([cx - 85, cy - 40, cx + 85, cy + 50], radius=8, fill='#3B4252', outline='#2E3440', width=3)
            draw.rectangle([cx - 30, cy - 60, cx + 10, cy - 40], fill='#4C566A')
            draw.ellipse([cx - 45, cy - 35, cx + 45, cy + 45], fill='#D8DEE9', outline='#81A1C1', width=6)
            draw.ellipse([cx - 25, cy - 15, cx + 25, cy + 25], fill='#2E3440')
            draw.rectangle([cx - 100, cy + 50, cx - 40, cy + 110], fill='#FFFFFF', outline='#D8DEE9', width=2)
            draw.rectangle([cx + 30, cy + 40, cx + 90, cy + 100], fill='#FFFFFF', outline='#D8DEE9', width=2)

        elif motif_key == "maze" or "새들" in title or "미로" in title:
            bg = '#111827'
            img = Image.new('RGB', (W, H), bg)
            draw = ImageDraw.Draw(img)
            cx, cy = W // 2, H // 2 - 20
            for s in range(5, 0, -1):
                r = s * 22
                draw.rectangle([cx - r, cy - r, cx + r, cy + r], outline='#10B981', width=3)
            draw.polygon([(cx, cy - 50), (cx - 30, cy - 80), (cx - 10, cy - 50), (cx + 30, cy - 80)], fill='#F9FAFB')

        elif motif_key == "glasses" or "안경 상점" in title:
            bg = '#FBF7F0'
            img = Image.new('RGB', (W, H), bg)
            draw = ImageDraw.Draw(img)
            cx, cy = W // 2, H // 2 - 20
            draw.polygon([(cx - 90, cy - 30), (cx, cy - 20), (cx, cy + 70), (cx - 90, cy + 60)], fill='#FFFDFA', outline='#D1C7BD')
            draw.polygon([(cx + 90, cy - 30), (cx, cy - 20), (cx, cy + 70), (cx + 90, cy + 60)], fill='#FFFDFA', outline='#D1C7BD')
            gold = '#B45309'
            draw.ellipse([cx - 65, cy - 20, cx - 15, cy + 30], outline=gold, width=4)
            draw.ellipse([cx + 15, cy - 20, cx + 65, cy + 30], outline=gold, width=4)
            draw.line([(cx - 15, cy), (cx + 15, cy)], fill=gold, width=3)

        elif motif_key == "monocle_map" or "잃어버린 항해" in title or "단안경" in title:
            bg = '#0F172A'
            img = Image.new('RGB', (W, H), bg)
            draw = ImageDraw.Draw(img)
            cx, cy = W // 2, H // 2 - 20
            draw.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], outline='#334155', width=2)
            draw.line([(cx - 90, cy), (cx + 90, cy)], fill='#334155', width=1)
            draw.line([(cx, cy - 90), (cx, cy + 90)], fill='#334155', width=1)
            draw.polygon([(cx - 70, cy + 40), (cx + 40, cy - 70), (cx + 60, cy - 50), (cx - 50, cy + 60)], fill='#F59E0B', outline='#B45309', width=2)

        elif "닳아버린 시선" in title:
            bg = '#181825'
            img = Image.new('RGB', (W, H), bg)
            draw = ImageDraw.Draw(img)
            cx, cy = W // 2, H // 2 - 20
            draw.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], outline='#CBA6F7', width=5, fill='#1E1E2E')
            draw.line([(cx + 50, cy + 50), (cx + 95, cy + 95)], fill='#CBA6F7', width=10)
            for _ in range(14):
                sx, sy = cx + rng.randint(-50, 50), cy + rng.randint(-50, 50)
                draw.ellipse([sx-2, sy-2, sx+2, sy+2], fill='#F9E2AF')

        elif motif_key == "fountain_pen" or "만년필" in title:
            bg = '#11111B'
            img = Image.new('RGB', (W, H), bg)
            draw = ImageDraw.Draw(img)
            cx, cy = W // 2, H // 2 - 20
            draw.polygon([(cx, cy + 40), (cx - 25, cy - 40), (cx, cy - 90), (cx + 25, cy - 40)], fill='#FAB387', outline='#F38BA8', width=2)
            draw.line([(cx, cy - 90), (cx, cy - 10)], fill='#11111B', width=2)
            draw.ellipse([cx - 15, cy + 50, cx + 15, cy + 80], fill='#89B4FA')
            draw.ellipse([cx - 50, cy + 60, cx + 50, cy + 120], outline='#45475A', width=3)

        else:
            bg_colors = ['#F8F6F0', '#181A24', '#0F172A', '#F4F1EA', '#1C1917']
            bg = rng.choice(bg_colors)
            img = Image.new('RGB', (W, H), bg)
            draw = ImageDraw.Draw(img)
            cx, cy = W // 2, H // 2 - 20
            c1 = rng.choice(['#E11D48', '#2563EB', '#059669', '#D97706', '#9333EA', '#0891B2'])
            c2 = rng.choice(['#F43F5E', '#3B82F6', '#10B981', '#F59E0B', '#A855F7', '#06B6D4'])
            shape_type = rng.choice(['orb', 'crystal', 'hourglass', 'lantern', 'compass'])
            
            if shape_type == 'orb':
                draw.ellipse([cx - 75, cy - 75, cx + 75, cy + 75], fill=c1, outline=c2, width=4)
                draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], outline='#FFFFFF', width=2)
            elif shape_type == 'crystal':
                draw.polygon([(cx, cy-90), (cx+60, cy-20), (cx+40, cy+70), (cx-40, cy+70), (cx-60, cy-20)], fill=c1, outline=c2, width=3)
            elif shape_type == 'hourglass':
                draw.polygon([(cx-60, cy-70), (cx+60, cy-70), (cx, cy), (cx+60, cy+70), (cx-60, cy+70)], fill=c1, outline=c2, width=3)
            elif shape_type == 'lantern':
                draw.rectangle([cx-45, cy-60, cx+45, cy+60], fill=c1, outline=c2, width=4)
                draw.polygon([(cx-45, cy-60), (cx, cy-90), (cx+45, cy-60)], fill=c2)
            else:
                draw.ellipse([cx-70, cy-70, cx+70, cy+70], outline=c1, width=5)
                draw.line([(cx-80, cy), (cx+80, cy)], fill=c2, width=3)
                draw.line([(cx, cy-80), (cx, cy+80)], fill=c2, width=3)

        img.save(filepath, "PNG", quality=95)
        print(f"[Editorial PIL] 고유 사물 표지 생성 완료: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"[Editorial PIL] 생성 에러: {e}")
        return False


async def generate_book_cover_art(title: str, genre: str, synopsis: str, color: str = "#b54a6a", unique_id: str = None, author: str = "") -> Optional[str]:
    """
    도서의 상징 사물 중심 편집 일러스트 표지를 100% 고유하게 생성합니다.
    1순위: Pollinations AI (고유 시드 적용)
    2순위: Editorial Vector PIL (도서 고유 맞춤 드로잉)
    """
    try:
        from PIL import Image
        os.makedirs("static/covers", exist_ok=True)
        if not unique_id:
            unique_id = secrets.token_hex(6)
        filename = f"cover_{unique_id}.png"
        filepath = os.path.join("static", "covers", filename)
        web_url = f"/static/covers/{filename}"

        if os.path.exists(filepath) and os.path.getsize(filepath) >= 5000:
            return web_url
        elif os.path.exists(filepath):
            os.remove(filepath)

        central_motif, motif_key = _extract_central_motif(title, genre, synopsis)

        # ── 1. Pollinations AI 생성 시도 ──
        prompt_text = (
            f"editorial concept art book cover illustration, "
            f"{central_motif}, "
            f"clean off-white background, centered composition, high quality Korean publication artwork, "
            f"3:4 portrait format, no text"
        )
        encoded_prompt = urllib.parse.quote(prompt_text)

        ai_success = False
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

        for attempt in range(2):
            # PYTHONHASHSEED에 따라 값이 매 프로세스마다 달라지는 내장 hash() 대신,
            # 결정적(deterministic)인 md5 해시로 시드를 계산하여 동일 도서는 항상 동일 시드가 나오도록 함
            seed_source = f"{title}{unique_id}{attempt}".encode("utf-8")
            seed = int(hashlib.md5(seed_source).hexdigest(), 16) % 999999 + 1000
            poll_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true&seed={seed}"
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.get(poll_url, headers=headers, timeout=25.0, follow_redirects=True)
                    if res.status_code == 200 and len(res.content) > 5000:
                        # 상태코드/용량만으로는 에러 페이지(HTML 등)를 그림으로 오인할 수 있으므로
                        # 실제로 디코딩 가능한 이미지인지 검증한 뒤에만 저장
                        try:
                            Image.open(io.BytesIO(res.content)).verify()
                        except Exception:
                            print(f"[Cover AI] attempt={attempt+1} 응답이 유효한 이미지가 아님 (size={len(res.content)}bytes) - 건너뜀")
                        else:
                            with open(filepath, "wb") as f:
                                f.write(res.content)
                            ai_success = True
                            print(f"[Cover AI] Pollinations 생성 성공 (attempt={attempt+1}): {web_url}")
                            break
                    else:
                        print(f"[Cover AI] attempt={attempt+1} 실패 응답 (status={res.status_code}, size={len(res.content)}bytes)")
            except Exception as e:
                print(f"[Cover AI] Attempt {attempt+1} 실패: {e}")
            await asyncio.sleep(1.5)

        # ── 2. AI 실패 시 Editorial PIL 백터 드로잉 생성 (100% 중복 없음) ──
        if not ai_success:
            print(f"[Cover Fallback] Editorial PIL 고유 사물 표지 생성: {title}")
            _generate_editorial_cover_pil(title, genre, synopsis, color, filepath, unique_id=unique_id, motif_key=motif_key)

        return web_url

    except Exception as ex:
        print(f"[Cover Generator] 표지 생성 실패 예외: {ex}")
        return None


def _delete_cover_file_if_exists(cover_image_url: Optional[str]):
    """도서/후보 삭제 시 더 이상 참조되지 않는 표지 파일을 디스크에서 함께 정리합니다."""
    if not cover_image_url:
        return
    try:
        cover_path = cover_image_url.lstrip("/").replace("/", os.sep)
        if os.path.exists(cover_path):
            os.remove(cover_path)
    except Exception as e:
        print(f"[Cover Cleanup] 표지 파일 삭제 실패: {e}")



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


RX_EMOJIS = ("❤️", "🤔", "😄", "✨")


def aggregate_reactions(db: Session, book_ids=None) -> dict:
    """도서별 채팅 반응 총합을 계산합니다.

    반응은 ChatMessage.reactions에 JSON 문자열(예: {"❤️": 3})로 저장되어
    SQL로 집계할 수 없기 때문에 파이썬에서 합산한다.
    예전에는 프론트에서 채팅 캐시(chatMsgs)를 훑어 집계했지만,
    그러면 채팅방을 한 번도 열지 않은 상태의 도서 상세 페이지에서
    항상 0으로 보이는 문제가 있어 서버 응답에 실어 보낸다.

    reactions가 비어 있지 않은 행만 조회하고, 목록 응답에서는
    book_ids를 모아 한 번에 질의해 N+1 쿼리를 피한다.
    """
    q = db.query(models.ChatMessage.book_id, models.ChatMessage.reactions).filter(
        models.ChatMessage.reactions.isnot(None),
        models.ChatMessage.reactions != "",
    )
    if book_ids is not None:
        if not book_ids:
            return {}
        q = q.filter(models.ChatMessage.book_id.in_(book_ids))

    totals = {}
    for book_id, raw in q.all():
        try:
            data = json.loads(raw)
        except (TypeError, ValueError):
            continue  # 손상된 JSON은 집계에서 제외한다
        if not isinstance(data, dict):
            continue
        bucket = totals.setdefault(book_id, {e: 0 for e in RX_EMOJIS})
        for emoji, count in data.items():
            # 서비스가 쓰는 4종 이모지만 집계한다.
            if emoji in bucket and isinstance(count, int) and count > 0:
                bucket[emoji] += count
    return totals


def serialize_book(b: "models.Book", db: Session, rx_totals: dict = None) -> dict:
    """Book 모델을 프론트엔드 응답용 dict로 직렬화합니다 (tags 파싱, 남은 기한, 참여자 수 계산 포함)."""
    book_dict = b.__dict__.copy()
    book_dict["tags"] = b.tags.split(",") if b.tags else []

    if b.created_at:
        delta = models.get_kst_now() - b.created_at
        remaining = b.deadline_days - delta.days
        book_dict["deadline_days"] = max(0, remaining)
    else:
        book_dict["deadline_days"] = b.deadline_days or 10

    # AI 사회자 및 관리자 계정은 "참여 중인 독자" 수에 포함하지 않는다.
    participant_count = db.query(func.count(func.distinct(models.ChatMessage.user_id))).join(
        models.User, models.ChatMessage.user_id == models.User.id
    ).filter(
        models.ChatMessage.book_id == b.id,
        models.User.is_admin == False,
        # AI 사회자(봇)는 참여 독자로 세지 않는다.
        # 역할 분리 이전에는 사회자가 is_admin=True라서 이 필터에 자연히 걸렸지만,
        # 지금은 is_admin=False / is_bot=True 이므로 봇 조건을 명시해야 한다.
        models.User.is_bot == False
    ).scalar()
    book_dict["participant_count"] = participant_count or 0

    # 채팅 반응 총합 — 도서 상세의 "지금 이 방의 반응" 줄이 사용한다.
    # 목록 응답은 미리 계산한 rx_totals를 넘겨받아 도서마다 질의하지 않는다.
    if rx_totals is None:
        rx_totals = aggregate_reactions(db, [b.id])
    book_dict["rx_counts"] = rx_totals.get(b.id, {e: 0 for e in RX_EMOJIS})
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
def get_or_create_moderator(db: Session):
    """
    AI 사회자 봇 계정을 반환한다(없으면 생성).

    역할 분리 원칙:
      - 사회자는 '채팅을 쓰는 봇'이지 '운영자'가 아니다 → is_bot=True, is_admin=False
      - 운영 권한은 config.OWNER_ADMIN_EMAIL 계정만 갖는다(enforce_roles 참고)
    """
    moderator = db.query(models.User).filter(models.User.email == MODERATOR_EMAIL).first()
    if not moderator:
        # 봇 계정은 로그인하지 않지만, password_hash 컬럼이 NOT NULL이라 임의의 난수를 넣어둔다.
        moderator = models.User(
            email=MODERATOR_EMAIL,
            nickname=MODERATOR_NICKNAME,
            password_hash=auth.get_password_hash(secrets.token_urlsafe(32)),
            is_admin=False,
            is_bot=True,
        )
        db.add(moderator)
        db.commit()
        db.refresh(moderator)
    else:
        changed = False
        if moderator.nickname != MODERATOR_NICKNAME:
            moderator.nickname = MODERATOR_NICKNAME
            changed = True
        if not moderator.is_bot:
            moderator.is_bot = True
            changed = True
        if moderator.is_admin:
            # 예전에는 사회자에게 관리자 권한을 강제로 부여했다. 이제는 회수한다.
            moderator.is_admin = False
            changed = True
        if changed:
            db.commit()
            db.refresh(moderator)
    return moderator


def enforce_roles(db: Session):
    """
    기동 시 계정 역할을 정리한다. (수동으로 DB를 고칠 필요가 없도록 코드가 상태를 보장한다)
      1. 운영자는 config.OWNER_ADMIN_EMAIL 한 명뿐 — 나머지 계정의 관리자 권한은 회수
      2. AI 사회자 봇은 하나뿐 — 중복 봇 계정의 메시지를 정식 봇으로 옮기고 계정을 삭제
    """
    moderator = get_or_create_moderator(db)

    # ── 1) 운영자 단일화 ──
    # 운영자 이메일이 지정되지 않았으면 권한을 건드리지 않는다.
    # (여기서 무조건 회수해 버리면 설정 하나 빠뜨렸을 때 아무도 관리자가 아니게 된다)
    if not config.OWNER_ADMIN_EMAIL:
        db.commit()
        return moderator

    owner = db.query(models.User).filter(models.User.email == config.OWNER_ADMIN_EMAIL).first()
    if owner and not owner.is_admin:
        owner.is_admin = True
        print(f"[Roles] 운영자 권한 부여: {owner.email}")
    if not owner:
        print(f"[Roles] 경고: 운영자 계정({config.OWNER_ADMIN_EMAIL})이 아직 가입하지 않았습니다.")

    revoked = db.query(models.User).filter(
        models.User.is_admin == True,
        models.User.email != config.OWNER_ADMIN_EMAIL,
    ).all()
    for u in revoked:
        u.is_admin = False
        print(f"[Roles] 관리자 권한 회수: {u.email} (닉네임: {u.nickname})")

    # ── 2) 사회자 봇 단일화 ──
    # 정식 봇이 아닌데 is_bot으로 표시된 계정만 봇 표시를 해제한다.
    #
    # 닉네임으로 판단하지 않는 이유:
    #   닉네임에 '사회자'가 들어갔다는 이유로 계정을 지우면, 그 닉네임으로 가입한 사람의
    #   글이 공식 사회자 발언으로 둔갑하고 계정·평점·서재가 영구 삭제된다.
    #   판단 근거는 오직 봇 플래그(그리고 MODERATOR_EMAIL)여야 한다.
    #
    # 계정을 삭제하지 않는 이유:
    #   기동 시 자동으로 도는 정리 작업이 사용자 데이터를 지우면 되돌릴 수 없다.
    #   권한만 낮추고, 실제 삭제가 필요하면 사람이 판단해서 하도록 남겨둔다.
    mislabeled = db.query(models.User).filter(
        models.User.id != moderator.id,
        models.User.is_bot == True,
    ).all()
    for dup in mislabeled:
        dup.is_bot = False
        msg_count = db.query(models.ChatMessage).filter(
            models.ChatMessage.user_id == dup.id
        ).count()
        print(f"[Roles] 봇 표시 해제: {dup.email} (메시지 {msg_count}건은 그대로 둠)")

    db.commit()
    return moderator

def seed_glass_shop_book_if_needed(db: Session):
    title = "오래된 안경 상점과 갈망의 정원"
    book = db.query(models.Book).filter(models.Book.title == title).first()
    if not book:
        book = models.Book(
            title=title,
            author="사키 쿠라타",
            genre="판타지",
            synopsis="마법이 사라진 마을 구석의 낡은 안경 상점. 수리공 아델은 타인의 감추고 싶은 속마음을 비추는 유리 안경을 발견한다. 안경을 쓸 때마다 마주하는 서늘한 진실과 갈망의 정원에서 펼쳐지는 잔혹하면서도 서정적인 힐링 대서사시.",
            tags="판타지,안경기억,잔혹동화,힐링",
            price="₩14,800",
            page_count=310,
            color="#b54a6a",
            endorsement_quote="가장 깊은 타인의 눈동자를 투영하는 아름답고 서늘한 마법 문학.",
            endorsement_attr="— 판타지 평론가 (익명)",
            publisher_review="타인의 진실과 무지의 평온 사이에서 갈등하는 우리 모두를 위한 깊은 사색의 서사시.",
            opening_line="안경 상점의 문을 열자, 오래된 유리 렌즈에 스민 아침 햇살과 서늘한 민트 향이 코끝을 스쳤다.",
            memorable_quote="타인의 속마음을 비추는 안경을 닦을 때마다, 나는 나의 고독을 닦아내고 있었다.",
            core_dilemma="Q. 타인의 숨겨진 진짜 마음에 닿는 안경이 있다면, 쓰시겠습니까 아니면 모른 채 살아가시겠습니까?",
            additional_questions="Q. 여주인공 아델이 유리 렌즈를 닦을 때 느꼈던 서늘한 죄책감의 정체는 무엇일까요?|Q. 당신에게 잊고 싶지 않은 인생의 '가장 선명한 순간'은 언제인가요?",
            characters="아델 — 안경 상점 수리공|헤이젤 — 갈망의 정원 파수꾼",
            deadline_days=10,
            is_archived=False
        )
        db.add(book)
        db.commit()
        db.refresh(book)

    msg_count = db.query(models.ChatMessage).filter(models.ChatMessage.book_id == book.id).count()
    if msg_count <= 1:
        readers_info = [
            ("달빛독자", "moonlight@gakong.com"),
            ("새벽사서", "dawn@gakong.com"),
            ("밤의활자", "night@gakong.com"),
            ("글꽃소녀", "flower@gakong.com"),
            ("구름산책", "cloud@gakong.com")
        ]
        user_map = {}
        for nick, email in readers_info:
            u = db.query(models.User).filter(models.User.nickname == nick).first()
            if not u:
                u = models.User(email=email, password_hash=auth.get_password_hash("password123"), nickname=nick)
                db.add(u)
                db.commit()
                db.refresh(u)
            user_map[nick] = u
            
        moderator = get_or_create_moderator(db)
        now_base = models.get_kst_now() - timedelta(minutes=60)
        
        # 1. AI 사회자 웰컴 카드
        q1_text = f"독자님, 『{book.title}』 독서방에 오신 것을 환영합니다!\n오늘 함께 나눌 추천 토론 질문입니다:\n\n1 타인의 숨겨진 진짜 마음에 닿는 안경이 있다면, 쓰시겠습니까 아니면 모른 채 살아가시겠습니까?\n2 여주인공 아델이 유리 렌즈를 닦을 때 느꼈던 서늘한 죄책감의 정체는 무엇일까요?\n3 당신에게 잊고 싶지 않은 인생의 '가장 선명한 순간'은 언제인가요?\n\n자유롭게 의견을 남기시거나 @사회자에게 이야기를 건네보세요!"
        m1 = models.ChatMessage(book_id=book.id, user_id=moderator.id, content=q1_text, created_at=now_base)
        db.add(m1)
        db.commit()
        db.refresh(m1)
        
        # 2. 달빛독자
        m2 = models.ChatMessage(book_id=book.id, user_id=user_map["달빛독자"].id, content="저라면 그 안경 절대 안 쓸 것 같아요... 타인의 속마음을 전부 알게 되면 상처만 받을 것 같아서요. 아델이 3장에서 안경을 쓰자마자 후회했던 장면에서 온몸에 돋은 소름이 아직도 안 가시네요.", created_at=now_base + timedelta(minutes=5))
        db.add(m2)
        db.commit()
        db.refresh(m2)
        
        # 3. 새벽사서 (m2 답장)
        m3 = models.ChatMessage(book_id=book.id, user_id=user_map["새벽사서"].id, content="달빛독자님 의견에 완전 동의해요! 저도 보면서 마음이 덜컥 내려앉았어요. 아델이 상점 주인의 경고를 무시하고 렌즈를 쓸어 올렸을 때 그 서늘함이란... 차라리 모르는 게 약이라는 문장이 이번 책을 관통하는 핵심 같아요.", reply_to_id=m2.id, created_at=now_base + timedelta(minutes=10))
        db.add(m3)
        db.commit()
        db.refresh(m3)
        
        # 4. 밤의활자 (m3 답장)
        m4 = models.ChatMessage(book_id=book.id, user_id=user_map["밤의활자"].id, content="하지만 저는 조금 생각이 달라요! 억울한 오해를 풀거나 사랑하는 사람의 아픔을 읽을 수 있다면 불편함을 감수하고라도 쓸 것 같아요. 4장 정원 씬에서 주인공이 진실을 깨닫고 눈물 흘리는 장면이 저한텐 최고의 명장면이었거든요", reply_to_id=m3.id, created_at=now_base + timedelta(minutes=15))
        db.add(m4)
        db.commit()
        db.refresh(m4)
        
        # 5. AI 사회자 (m4 답장)
        m5 = models.ChatMessage(book_id=book.id, user_id=moderator.id, content="밤의활자님, 진실을 감당하려는 그 용기 있는 관점이 참으로 눈부십니다. 타인의 아픔에 기꺼이 손을 뻗으려는 밤의활자님의 따스한 마음이 4장 정원의 햇살과 닮아있네요.\n\n글꽃소녀님과 구름산책님은 진실과 평온 중 어느 쪽에 더 마음이 기우시나요?", reply_to_id=m4.id, created_at=now_base + timedelta(minutes=20))
        db.add(m5)
        db.commit()
        db.refresh(m5)
        
        # 6. 글꽃소녀 (m5 답장)
        m6 = models.ChatMessage(book_id=book.id, user_id=user_map["글꽃소녀"].id, content="@사회자님! 저는 밤의활자님과 달빛독자님 중간인 것 같아요! 쓰긴 쓰되, 진짜 중요한 선택의 순간에만 아주 잠깐 쓸 것 같아요 ㅋㅋㅋ 아델이 안경을 닦을 때마다 나던 그 특유의 민트 향 묘사도 진짜 좋았어요.", reply_to_id=m5.id, created_at=now_base + timedelta(minutes=25))
        db.add(m6)
        db.commit()
        db.refresh(m6)


def seed_lost_voyage_book_if_needed(db: Session):
    title = "깨진 렌즈가 비춘 잃어버린 항해"
    book = db.query(models.Book).filter(models.Book.title == title).first()
    if not book:
        book = models.Book(
            title=title,
            author="지도제작자 테오 (가상)",
            genre="에세이/비문학",
            synopsis="꿈의 조각가이자 지도 제작자 테오. 그가 낡고 깨진 단안경으로 그림자를 그리면, 렌즈 너머로 보이지 않는 잊혀진 항해의 해도가 서서히 모습을 드러낸다. 거친 안개 미궁 속에서 외면당한 경고와 다가오는 비극의 파편을 엮어내어 세상을 위험에서 구하고 창조와 해체의 평화를 되찾는 웅장한 서정 대서사시.",
            tags="단안경,잊혀진항해,안개미궁,기억의해도를찾아서",
            price="₩16,500",
            page_count=510,
            color="#3e2723",
            endorsement_quote="상처 입은 렌즈 너머로 잊혀진 타인의 궤적을 받아안는 눈부신 문학적 유영.",
            endorsement_attr="— 해양문학 평론가 (익명)",
            publisher_review="잊혀진 파편의 해도를 따라 거친 안개 미궁을 헤쳐나가는 우리 모두를 위한 영혼의 지도.",
            opening_line="낡고 깨진 단안경을 쓸어 올릴 때마다, 유리 렌즈에 스민 아침 햇살 너머로 보이지 않는 운명의 해도가 그려지기 시작했다.",
            memorable_quote="바다는 모든 것을 씻어내어 기억하지 않아도, 나의 해도는 끝내 너의 궤적을 기억한다.",
            core_dilemma="Q. 잊혀진 과거의 비극을 알려주는 파편의 해도를 따라 위험천만한 항해를 계속해야 할까요, 아니면 현실의 평온을 지켜야 할까요?",
            additional_questions="Q. 테오의 깨진 단안경이 의미하는 상처와 기억의 연관성은 무엇일까요?|Q. 거친 안개 미궁 속에서 당신이 포기하지 않고 지키고 싶은 가장 소중한 항해의 궤적은 무엇인가요?",
            characters="테오 — 꿈과 기억의 지도 제작자|셀레나 — 그림자를 녹이는 만년필의 조각가",
            deadline_days=9999,
            is_archived=False
        )
        db.add(book)
        db.commit()
        db.refresh(book)
    elif book.deadline_days != 9999 or book.is_archived:
        # deadline_days=9999/is_archived=False 상시 활성화 로직이 추가되기 전 생성된 레코드가
        # 일반 10일 만료 규칙에 걸려 자동 아카이브된 경우, 영구 활성 샘플 독서방 상태로 복구
        book.deadline_days = 9999
        book.is_archived = False
        db.commit()

    msg_count = db.query(models.ChatMessage).filter(models.ChatMessage.book_id == book.id).count()
    if msg_count <= 2:
        db.query(models.ChatMessage).filter(models.ChatMessage.book_id == book.id).delete()
        db.commit()

        moderator = get_or_create_moderator(db)
        
        readers_info = [
            ("바다의항해자", "voyage@gakong.com"),
            ("단안경사색가", "monocle@gakong.com"),
            ("해도의파수꾼", "mapkeeper@gakong.com"),
            ("문학유영가", "swimmer@gakong.com"),
            ("꿈꾸는선장", "captain@gakong.com"),
            ("유리렌즈의비밀", "lens@gakong.com"),
            ("항해사김민준", "minjun@gakong.com")
        ]
        user_map = {}
        for nick, email in readers_info:
            u = db.query(models.User).filter(models.User.nickname == nick).first()
            if not u:
                u = models.User(email=email, password_hash=auth.get_password_hash("password123"), nickname=nick)
                db.add(u)
                db.commit()
                db.refresh(u)
            user_map[nick] = u

        dt_july29_1 = datetime(2026, 7, 29, 10, 15, 0)
        dt_july29_2 = datetime(2026, 7, 29, 14, 20, 0)
        dt_july29_3 = datetime(2026, 7, 29, 19, 40, 0)

        dt_july30_1 = datetime(2026, 7, 30, 11, 10, 0)
        dt_july30_2 = datetime(2026, 7, 30, 16, 30, 0)
        dt_july30_3 = datetime(2026, 7, 30, 21, 5, 0)

        dt_july31_1 = datetime(2026, 7, 31, 9, 40, 0)
        dt_july31_2 = datetime(2026, 7, 31, 11, 0, 0)
        dt_july31_3 = datetime(2026, 7, 31, 13, 15, 0)
        dt_july31_4 = datetime(2026, 7, 31, 14, 5, 0)

        # Day 1: 7월 29일 (수)
        m1 = models.ChatMessage(book_id=book.id, user_id=user_map["바다의항해자"].id, content="지도 제작자 테오가 낡고 깨진 단안경을 닦을 때마다 렌즈 너머로 보이지 않는 운명의 해도가 그려지는 1장 도입부부터 몰입감이 진짜 대단하네요!", created_at=dt_july29_1)
        db.add(m1); db.commit(); db.refresh(m1)

        m2 = models.ChatMessage(book_id=book.id, user_id=user_map["단안경사색가"].id, content="맞아요! 렌즈에 금이 간 이유가 과거 거대한 폭풍우를 경고하다 깨진 것이란 비하인드를 읽고 소름 돋았습니다. 흩어진 해도의 조각들이 주인공 테오의 잊혀진 기억 자체였군요.", created_at=dt_july29_2)
        db.add(m2); db.commit(); db.refresh(m2)

        m3 = models.ChatMessage(book_id=book.id, user_id=user_map["해도의파수꾼"].id, content="단안경사색가님 관점에 완전 공감해요! 렌즈의 깨진 균열 선이 지도 상의 위험 해역 좌표와 딱 맞아떨어지는 연출이 참 고혹적이었어요", reply_to_id=m2.id, created_at=dt_july29_3)
        db.add(m3); db.commit(); db.refresh(m3)

        # Day 2: 7월 30일 (목)
        m4 = models.ChatMessage(book_id=book.id, user_id=user_map["문학유영가"].id, content="2장 안개 미궁 씬에서 동료들이 '이 이상 나아가면 파멸'이라고 외면할 때, 테오 혼자 단안경을 쥐고 선두에 서는 장면에서 눈물이 핑 돌았어요 차라리 현실의 평온을 택할 순 없었을까요?", created_at=dt_july30_1)
        db.add(m4); db.commit(); db.refresh(m4)

        m5 = models.ChatMessage(book_id=book.id, user_id=user_map["꿈꾸는선장"].id, content="저는 테오의 선택을 지지해요! 진실을 외면한 평화는 언젠가 무너지는 모래성 같으니까요. 렌즈 너머로 비친 동료들의 진짜 갈망을 읽었기에 멈출 수 없었던 거죠.", reply_to_id=m4.id, created_at=dt_july30_2)
        db.add(m5); db.commit(); db.refresh(m5)

        m6 = models.ChatMessage(book_id=book.id, user_id=user_map["유리렌즈의비밀"].id, content="꿈꾸는선장님 말씀대로 2장의 시련은 단순한 항해가 아니라 스스로의 본 모습을 찾아가는 사색의 시련이었던 것 같아요", reply_to_id=m5.id, created_at=dt_july30_3)
        db.add(m6); db.commit(); db.refresh(m6)

        # Day 3: 7월 31일 (금)
        m7 = models.ChatMessage(book_id=book.id, user_id=user_map["항해사김민준"].id, content="'바다는 모든 것을 씻어내어 기억하지 않아도, 나의 해도는 끝내 너의 궤적을 기억한다' ... 3장 피날레 문장에 가슴이 먹먹해집니다. @사회자 님은 테오의 이 잃어버린 항해를 어떤 의미로 보시나요?", created_at=dt_july31_1)
        db.add(m7); db.commit(); db.refresh(m7)

        m8 = models.ChatMessage(book_id=book.id, user_id=moderator.id, content="항해사김민준님, 깊은 사색이 담긴 인상적인 문장을 짚어주셨네요. 테오에게 깨진 단안경은 과거의 상처를 들추는 아픔이 아니라, 잊혀진 사람들의 소망을 현실의 평화로 엮어내는 숭고한 창조의 계기였습니다.\n\n바다의항해자님과 단안경사색가님은 테오가 항해의 끝에서 되찾은 가장 소중한 궤적이 무엇이라고 생각하시나요?", reply_to_id=m7.id, created_at=dt_july31_2)
        db.add(m8); db.commit(); db.refresh(m8)

        m9 = models.ChatMessage(book_id=book.id, user_id=user_map["바다의항해자"].id, content="@사회자님! 테오가 되찾은 건 단순한 지도가 아니라 '함께 항해했던 동료들에 대한 깊은 신뢰'였다고 생각해요 3장 마지막 햇살 씬이 그래서 너무 따뜻했습니다.", reply_to_id=m8.id, created_at=dt_july31_3)
        db.add(m9); db.commit(); db.refresh(m9)

        m10 = models.ChatMessage(book_id=book.id, user_id=user_map["단안경사색가"].id, content="맞아요! 상처 입은 렌즈로 보았기에 비로소 타인의 아픔을 가장 온전하게 품을 수 있었던 테오의 눈빛이 오래도록 잔상으로 남네요. 역대 최고의 활성화 독서방이었습니다", reply_to_id=m9.id, created_at=dt_july31_4)
        db.add(m10); db.commit(); db.refresh(m10)

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
            
        moderator = db.query(models.User).filter(models.User.email == MODERATOR_EMAIL).first()
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
                당신은 '가공독서회(Gakong Reading Club)'의 따뜻하고 감성 넘치는 'AI 사회자'입니다.
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
                
                [수행할 작업: 3단계 샌드위치 응답 공식]
                1단계 (공감 1문장): 독자({user_message.user.nickname}님)의 인상적인 통찰이나 감상에 따뜻하게 공감하며 닉네임을 불러 다정하게 칭찬합니다.
                2단계 (상상/세계관 1문장): 독자의 의견에 이어 『{book.title}』의 세계관, 숨겨진 미공개 비하인드, 또는 인물의 심리에 흥미로운 살을 붙여 상상 디테일을 제공합니다.
                3단계 (대화 확장 1문장): 대화를 계속 이어갈 수 있는 가벼운 질문이나 화두를 던지며 정갈하게 대답을 마무리합니다.
                
                [조건]
                1. 존댓말을 사용하고, 정중하면서도 가슴 따뜻해지는 감성적인 어조를 유지하세요.
                2. 독자의 닉네임({user_message.user.nickname}님)을 칭찬하며 다정하게 불러주세요.
                3. ⚠️ [글자수 제한 없음] 글자수나 문장 수에 제한 없이, 독자의 감상과 질문에 대해 충분히 정성스럽고 풍성하게 대답을 작성하세요.
                4. ⚠️ [필수] 모든 문장은 반드시 마침표(.), 느낌표(!), 또는 물음표(?)로 깔끔하고 완벽하게 마감해야 합니다.
                5. 마크다운 기호나 부연설명 없이 오직 사회자 답변 텍스트만 출력하세요.
                6. [필수] 이모지와 이모티콘을 절대 사용하지 마세요. 감정은 문장으로만 표현합니다.
                """
            else:
                prompt = f"""
                당신은 '가공독서회(Gakong Reading Club)'의 깔끔하고 정갈한 'AI 사회자'입니다.
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
                장황한 공감이나 사족, 과도한 개입을 철저히 배제하고, 독자들이 상상력과 토론을 자연스럽게 이어갈 수 있도록 돕는 '명확하고 깊이 있는 토론 질문'을 정갈하게 던지세요.
                
                [조건]
                1. 과도한 칭찬이나 긴 사족을 절대 붙이지 말고 담백하고 정중하게 작성하세요.
                2. 최근 대화의 흐름이나 핵심 소재(딜레마, 인물의 선택 등)에 어울리는 본질적인 질문을 던지세요.
                3. ⚠️ [필수] 모든 문장은 반드시 마침표(.)나 물음표(?)로 정돈되게 끝내야 합니다.
                4. 마크다운 기호나 부연설명 없이 오직 사회자의 담백한 질문 멘트 텍스트만 출력하세요.
                5. [필수] 이모지와 이모티콘을 절대 사용하지 마세요. 감정은 문장으로만 표현합니다.
                """
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 4096
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
                
        # DB 저장 (문장이 잘리지 않도록 안전 마감 처리)
        final_content = moderator_content.strip()
        
        # 채팅 본문에는 이모지를 쓰지 않는다 (프롬프트로도 금지했지만 최종 방어선)
        final_content = strip_chat_emoji(final_content)

        # 문장 끝에 문장부호가 누락된 경우 안전하게 마침표 추가 (절대 이전 문장으로 자르지 않음)
        if final_content and not final_content[-1] in ['.', '?', '!', '"', "'", '⟩', '»']:
            final_content = final_content + "."

        db_msg = models.ChatMessage(
            book_id=book_id,
            user_id=moderator.id,
            content=final_content,
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

    # 앱 시작 시: 활성 독서방 자동 보충 백그라운드 루프 가동
    asyncio.create_task(auto_refill_loop())
    print("Auto refill background loop started.")

    # AI 사회자 계정 및 시드 독서방 자동 생성
    db = database.SessionLocal()
    try:
        # 스키마 패치를 가장 먼저 — 아래 시드가 새 컬럼을 쓸 수 있다
        apply_schema_patches()
        enforce_roles(db)
        seed_glass_shop_book_if_needed(db)
        seed_lost_voyage_book_if_needed(db)
        seed_fountain_pen_book_if_needed(db)
        seed_faded_gaze_book_if_needed(db)
        print("AI Moderator & Book Seeds initialized successfully.")
    except Exception as e:
        print(f"Error initializing AI Moderator or Seed data: {e}")
    finally:
        db.close()

    # ── 앱 시작 직후: 표지 없는 모든 Book에 AI 표지 백그라운드 자동 생성 ──
    async def _generate_missing_book_covers():
        await asyncio.sleep(2)  # DB 초기화 안정화 대기
        bg_db = database.SessionLocal()
        try:
            books_no_cover = bg_db.query(models.Book).filter(
                (models.Book.cover_image_url == None) | (models.Book.cover_image_url == "")
            ).all()
            if not books_no_cover:
                print("[Cover Init] 모든 Book에 표지가 있습니다.")
                return
            print(f"[Cover Init] 표지 없는 Book {len(books_no_cover)}권 AI 표지 생성 시작...")
            results = await asyncio.gather(*[
                generate_book_cover_art(b.title, b.genre, b.synopsis, b.color, f"book_{b.id}", author=b.author or "")
                for b in books_no_cover
            ], return_exceptions=True)
            updated = 0
            for book, url in zip(books_no_cover, results):
                if isinstance(url, Exception):
                    print(f"[Cover Init] book_id={book.id} 표지 생성 실패: {url}")
                    continue
                if url:
                    book.cover_image_url = url
                    updated += 1
            bg_db.commit()
            print(f"[Cover Init] {updated}권 표지 생성 완료.")
        except Exception as e:
            print(f"[Cover Init] 백그라운드 표지 초기화 오류: {e}")
        finally:
            bg_db.close()

    asyncio.create_task(_generate_missing_book_covers())

    yield  # 앱 실행 중
    # 앱 종료 시 필요한 정리 작업이 있다면 여기에 추가

app = FastAPI(
    title="가공독서회 (Gakong) API Server",
    description="FastAPI + MySQL + WebSockets + Gemini API 기반 백엔드 서비스",
    version="1.0.0",
    lifespan=lifespan,
    # 운영에서는 API 스키마 문서를 노출하지 않는다.
    docs_url=None if config.IS_PRODUCTION else "/docs",
    redoc_url=None if config.IS_PRODUCTION else "/redoc",
    openapi_url=None if config.IS_PRODUCTION else "/openapi.json",
)

# 모든 응답에 CSP 등 공통 보안 헤더를 부착한다 (security.py에서 정책 일괄 관리).
app.add_middleware(security.SecurityHeadersMiddleware, is_production=config.IS_PRODUCTION)

# CORS: 허용 출처는 config.ALLOW_ORIGINS(.env의 ALLOW_ORIGINS)로만 지정한다.
# 프론트엔드를 이 서버가 직접 서빙하므로 기본값은 로컬 개발 출처뿐이며 와일드카드는 금지된다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOW_ORIGINS,
    allow_origin_regex=config.ALLOW_ORIGIN_REGEX,
    # 인증은 쿠키가 아닌 Authorization 헤더(Bearer 토큰)로만 이루어지므로 자격증명 허용은 불필요하다.
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
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
    # 닉네임은 시스템이 배정하는 값이지만, API를 직접 호출하는 악의적 요청으로부터 보호하기 위해
    # 한글/영문/숫자만 허용하고 길이를 제한한다 (HTML/script 삽입을 통한 저장형 XSS 방지).
    nickname: str = Field(
        ...,
        min_length=1,
        max_length=20,
        pattern=r'^[가-힣a-zA-Z0-9]+$',
        description="닉네임은 한글/영문/숫자만 사용하여 1~20자로 입력해야 합니다."
    )

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

HTML_FILE_PATH = os.path.join(os.path.dirname(__file__), "index_standalone.html")



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
def signup(user_data: UserSignup, request: Request, db: Session = Depends(database.get_db)):
    # 0. 동일 IP에서의 대량 계정 생성 차단
    if (user_data.email or "").strip().lower().endswith(SAMPLE_EMAIL_DOMAIN):
        # 시드 독자 도메인은 서비스 소개용 계정 전용이다.
        raise HTTPException(status_code=400, detail="사용할 수 없는 이메일 도메인입니다.")
    SIGNUP_LIMITER.hit(security.client_ip(request))

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


# ── 인증 관련 레이트리밋 정책 ──
# 정책은 여기서 한눈에 보이도록 모아두고, 구현은 security.RateLimiter가 담당한다.
#
# 로그인 제한을 IP와 계정 두 축으로 나눈 이유:
#   - IP 기준(엄격): 한 곳에서 비밀번호를 찍어보는 공격을 빠르게 막는다.
#   - 계정 기준(느슨): 분산 공격도 막되, 공격자가 남의 이메일로 실패를 쌓아
#     피해자를 손쉽게 로그인 불가 상태로 만드는 것(DoS)은 어렵게 한다.
LOGIN_IP_LIMITER = security.RateLimiter(
    max_attempts=10, window_seconds=15 * 60,
    message="로그인 시도가 너무 많습니다. {minutes}분 후 다시 시도해주세요.",
)
LOGIN_ACCOUNT_LIMITER = security.RateLimiter(
    max_attempts=20, window_seconds=15 * 60,
    message="이 계정에 대한 로그인 시도가 너무 많습니다. {minutes}분 후 다시 시도해주세요.",
)
SIGNUP_LIMITER = security.RateLimiter(
    max_attempts=5, window_seconds=60 * 60,
    message="회원가입 요청이 너무 많습니다. {minutes}분 후 다시 시도해주세요.",
)
PASSWORD_RESET_LIMITER = security.RateLimiter(
    max_attempts=3, window_seconds=60 * 60,
    message="비밀번호 재설정 요청이 너무 많습니다. {minutes}분 후 다시 시도해주세요.",
)
# 링크 '발송 요청'과 링크를 받은 뒤의 '비밀번호 제출'은 제한기를 나눠야 한다.
# 같은 제한기를 쓰면, 메일을 3번 요청한 사람이 정작 링크를 눌러 새 비밀번호를 넣을 때 막힌다.
PASSWORD_SUBMIT_LIMITER = security.RateLimiter(
    max_attempts=10, window_seconds=60 * 60,
    message="비밀번호 재설정 시도가 너무 많습니다. {minutes}분 후 다시 시도해주세요.",
)


@app.post("/api/auth/login", response_model=TokenResponse)
def login(login_data: UserLogin, request: Request, db: Session = Depends(database.get_db)):
    # 0. 최근 실패 횟수 기반 잠금 여부 확인 (IP · 계정 두 축)
    ip = security.client_ip(request)
    email_key = login_data.email.lower()
    LOGIN_IP_LIMITER.check(ip)
    LOGIN_ACCOUNT_LIMITER.check(email_key)

    # 1. 회원 정보 조회
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    if not user or not auth.verify_password(login_data.password, user.password_hash):
        LOGIN_IP_LIMITER.record(ip)
        LOGIN_ACCOUNT_LIMITER.record(email_key)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )

    # 봇 계정(AI 사회자)은 사람이 로그인할 수 없다 — 공식 계정 사칭 차단
    if user.is_bot:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="이 계정으로는 로그인할 수 없습니다."
        )

    # 로그인 성공 시 실패 기록 초기화
    LOGIN_IP_LIMITER.reset(ip)
    LOGIN_ACCOUNT_LIMITER.reset(email_key)

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
        
    # 2. 새 비밀번호 적용 (기존에 발급된 토큰은 auth.set_password가 무효화 처리)
    auth.set_password(user, req.new_password)
    db.commit()
    return {"message": "비밀번호가 성공적으로 변경되었습니다. 다시 로그인해 주세요. 🔒"}


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


BR = chr(10)  # 메일 본문 줄바꿈

# ── 비밀번호 재설정 링크 발송 유틸리티 ──
#
# 예전에는 요청만 하면 즉시 임시 비밀번호로 교체했다. 이메일만 알면 아무나 남의 계정을
# 잠글 수 있었기 때문에, "메일의 링크를 눌러야 실제로 바뀌는" 방식으로 변경했다.
# SMTP 설정 유틸은 config에서 읽는다.

def _send_email(to_email: str, subject: str, body: str) -> bool:
    """메일 1통을 발송한다. 발송 성공 여부를 반환한다."""
    if not config.SMTP_CONFIGURED:
        print(f"[SMTP 미설정] {to_email} 에게 보낼 메일을 발송하지 못했습니다. .env의 SMTP_* 설정을 확인하세요.")
        return False
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = config.SMTP_FROM_EMAIL
        msg["To"] = to_email
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT, timeout=15) as server:
            server.starttls()  # TLS 보안 활성화
            server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
            server.sendmail(config.SMTP_FROM_EMAIL, [to_email], msg.as_string())
        print(f"[SMTP 발송 완료] 수신인: {to_email}")
        return True
    except Exception as e:
        # 예외 메시지에 자격증명이 섞이지 않도록 예외 종류만 남긴다.
        print(f"[SMTP 발송 실패] 수신인: {to_email} - 오류 유형: {type(e).__name__}")
        return False


def send_reset_link_email(to_email: str, nickname: str, reset_url: str):
    """비밀번호 재설정 링크를 메일로 발송합니다."""
    body = (
        f"안녕하세요, {nickname} 독자님." + BR * 2 +
        "비밀번호 재설정을 요청하셨습니다. 아래 링크에서 새 비밀번호를 설정해 주세요." + BR * 2 +
        reset_url + BR * 2 +
        f"이 링크는 {config.PASSWORD_RESET_TTL_MINUTES}분 후 만료되며 한 번만 사용할 수 있습니다." + BR +
        "본인이 요청하지 않았다면 이 메일을 무시하셔도 됩니다. 기존 비밀번호는 그대로 유지됩니다." + BR * 2 +
        "가공독서회 운영진 드림"
    )
    sent = _send_email(to_email, "[가공독서회] 비밀번호 재설정 링크입니다.", body)
    if not sent and not config.IS_PRODUCTION:
        # 개발 환경에서만 링크를 콘솔로 확인할 수 있게 한다 (운영에서는 절대 출력하지 않는다).
        print(f"[개발용 재설정 링크] {to_email} -> {reset_url}")


@app.post("/api/auth/find-password")
def find_password(
    req: FindPasswordRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db)
):
    """
    비밀번호 재설정 링크를 가입 이메일로 발송합니다.

    보안상 두 가지 원칙을 지킨다:
      1. 가입 여부와 무관하게 항상 동일한 응답을 준다 (가입자 이메일 열거 방지).
      2. 이 요청만으로는 비밀번호가 바뀌지 않는다. 메일의 링크를 눌러야 실제로 변경된다.
    """
    # 대량 요청 차단 (IP · 이메일 두 축)
    PASSWORD_RESET_LIMITER.hit(security.client_ip(request))
    PASSWORD_RESET_LIMITER.hit(req.email.lower())

    user = db.query(models.User).filter(models.User.email == req.email).first()
    if user:
        raw_token = auth.issue_reset_token(user)
        db.commit()
        reset_url = f"{config.APP_BASE_URL}/reset-password?token={raw_token}"
        # 응답 지연 없이 백그라운드에서 발송
        background_tasks.add_task(
            send_reset_link_email,
            to_email=user.email,
            nickname=user.nickname,
            reset_url=reset_url,
        )

    return {
        "message": (
            "가입된 이메일이라면 비밀번호 재설정 링크를 보냈습니다. 메일함을 확인해 주세요. ✉️"
        )
    }


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=10, description="메일로 받은 재설정 토큰")
    new_password: str = Field(..., min_length=8, description="새 비밀번호는 최소 8자 이상이어야 합니다.")


@app.post("/api/auth/reset-password")
def reset_password(
    req: ResetPasswordRequest,
    request: Request,
    db: Session = Depends(database.get_db)
):
    """메일로 받은 1회용 토큰을 검증하고 새 비밀번호를 적용합니다."""
    ip = security.client_ip(request)
    PASSWORD_SUBMIT_LIMITER.check(ip)

    try:
        user = auth.consume_reset_token(db, req.token)
    except HTTPException:
        # 토큰을 틀린 경우에만 시도 횟수를 센다(무작위 토큰 대입 방어).
        PASSWORD_SUBMIT_LIMITER.record(ip)
        raise
    auth.set_password(user, req.new_password)  # 기존 발급 토큰도 함께 무효화
    auth.clear_reset_token(user)               # 재설정 토큰은 1회용
    db.commit()
    PASSWORD_SUBMIT_LIMITER.reset(ip)          # 정상 처리됐으면 시도 기록을 비운다
    return {"message": "비밀번호가 변경되었습니다. 새 비밀번호로 로그인해 주세요. 🔒"}


@app.get("/reset-password", response_class=HTMLResponse, include_in_schema=False)
async def serve_reset_password_page(request: Request):
    """메일 링크로 진입하는 비밀번호 재설정 페이지."""
    return templates.TemplateResponse(request=request, name="reset_password.html")



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
async def generate_candidates(
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db),
    current_user_id: int = Depends(auth.get_current_user_id)
):
    """
    Google Gemini API를 호출하여 세상에 없는 독창적인 책을 실시간 생성하거나 Pool에서 가져와 3개의 후보를 반환합니다.
    로그인한 사용자에 한해, 무분별한 생성을 막기 위해 1일 1회로 제한합니다.
    """
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인이 필요한 서비스입니다.")

    # 아직 고르지 않은 후보가 있으면 새로 만들지 않고 그대로 돌려준다.
    # (고르지 않은 채 화면을 벗어났다가 다시 들어온 경우 — 하루 제한도 소모하지 않는다)
    existing = db.query(models.CandidateBook).filter(
        models.CandidateBook.status == "pending",
        models.CandidateBook.created_by == current_user_id,
    ).order_by(models.CandidateBook.id).all()
    if existing:
        return [serialize_candidate(c) for c in existing]

    now_kst = models.get_kst_now()
    if user.last_generation_at and user.last_generation_at.date() == now_kst.date():
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="새 책 생성은 하루에 한 번만 가능합니다. 내일 다시 시도해 주세요! 📖"
        )

    final_candidates = await _produce_candidate_books(db, background_tasks, owner_user_id=current_user_id)

    # 커밋하면 ORM 객체가 만료되므로, 응답에 쓸 값은 커밋 전에 확보해 둔다.
    payload = [serialize_candidate(c) for c in final_candidates]

    # 생성 성공 시에만 1일 1회 제한 기록을 갱신
    user.last_generation_at = now_kst
    db.commit()
    return payload


async def _produce_candidate_books(db: Session, background_tasks: BackgroundTasks,
                                   owner_user_id: Optional[int] = None,
                                   count: int = 3) -> list:
    """
    Pool(보관함)에서 재사용 가능한 후보를 우선 꺼내오고, 부족한 만큼만 Gemini(실패 시 폴백 템플릿)로
    새로 생성하여 count권(기본 3권)의 CandidateBook 레코드를 만듭니다. 표지 생성은 백그라운드로 분리합니다.
    사람이 누르는 "새 책 생성" 엔드포인트와 활성 독서방 자동 보충 백그라운드 잡이 공통으로 재사용합니다.
    """
    genres = [
        '로맨스 판타지', '청춘/로맨스', '힐링/일상소설', '코믹/유머 에세이', 
        'SF/스페이스 탐험', '추리/미스터리', '판타지 모험', '철학적 에세이', '드라마/성장소설'
    ]
    tones = [
        '설렘 가득하고 풋풋한 핑크빛 로맨스 톤',
        '위트 있고 유쾌하며 웃음을 유발하는 경쾌한 톤',
        '따스한 햇살 아래 따뜻하고 가슴 포근해지는 힐링 톤',
        '화려하고 신비로운 마법 세계의 로맨스 판타지 분위기',
        '스릴과 흥미진진한 미스터리가 어우러진 긴장감 넘치는 톤',
        '낭만적이고 가슴 벅찬 우주 탐험의 정열적인 분위기',
        '청춘의 찬란함과 빛나는 고백이 담긴 감성적 톤',
        '기묘하고 잔혹동화 같은 매혹적인 판타지 분위기',
        '깊이 있는 사색과 삶의 위로를 전하는 따뜻한 철학적 톤'
    ]
    kw_abstract = [
        '설렘', '첫사랑', '기적', '약속', '달콤한 고백', '비밀의 시간', '찬란한 청춘', 
        '행운', '무지개 빛 희망', '해피엔딩', '새로운 출발', '웃음과 눈물', '빛나는 순간',
        '마법의 계약', '평행 우주', '자아의 증발', '우연의 일치', '잔잔한 평화', '해방', 
        '눈부신 각성', '영원한 우정', '속속들이 아는 사이', '갈망', '순수', '운명적인 만남', 
        '선택', '동경', '구원', '열정', '용기', '뜻밖의 선물', '달콤한 오해'
    ]
    kw_concrete = [
        '분홍빛 마법 지팡이', '디저트 카페', '스타후르츠 파이', '무지개 고양이', '에메랄드 왕관', 
        '달콤한 딸기 타르트', '비밀의 화원', '별빛 우주선', '고양이 카페', '빛나는 보석 상자',
        '찻잔과 민들레', '시계태엽 고래', '하늘을 나는 도서관', '모래시계', '은빛 조개껍데기',
        '손때 묻은 지도', '빨간 우체통', '오르골 상자', '빈티지 카메라', '비밀 일기장', 
        '회중시계', '흔들의자', '망원경', '체스판', '지구본', '해시계', '촛대', '하트 펜던트',
        '달콤한 향수', '비밀의 열쇠', '구름 베이커리', '은하수 티켓'
    ]

    selected_genre = random.choice(genres)
    selected_tone = random.choice(tones)
    k1 = random.choice(kw_abstract)
    k2 = random.choice(kw_concrete)
    
    # 0. 같은 사용자가 이전에 받아놓고 고르지 않은 후보는 pool로 되돌린다.
    #    (다른 사람이 고르는 중인 후보까지 건드리지 않도록 소유자 기준으로만 정리한다)
    stale = db.query(models.CandidateBook).filter(models.CandidateBook.status == 'pending')
    if owner_user_id is not None:
        stale = stale.filter(models.CandidateBook.created_by == owner_user_id)
    stale.update({"status": "pool"}, synchronize_session=False)
    db.flush()

    # 1. Pool(보관된 남겨진 책들) 중에서 매번 무작위 랜덤으로 꺼내오기 (최대 3권)
    reused_candidates = db.query(models.CandidateBook).filter(
        models.CandidateBook.status == 'pool'
    ).order_by(
        func.random()
    ).limit(count).all()
    
    needed_count = count - len(reused_candidates)
    
    # Gemini용 프롬프트 조립 (백엔드 AI 100% 자율 몰입 데이터 생성 프롬프트)
    prompt = f"""
    당신은 가공독서회(Gakong Reading Club)를 위한 천재적이고 감각적인 가상 도서 에디터이자 문학 평론가입니다.

    [생성 조건]
    - 장르: {selected_genre}
    - 분위기/어조: {selected_tone}
    - 핵심 소재 1 (추상적 테마): {k1}
    - 핵심 소재 2 (구체적 사물/장소): {k2}
    - 생성 개수: 정확히 {needed_count}권

    [💡 소재 발상 및 기획 5가지 원칙 (Steemit 글쓰기 기법 반영)]
    1. **독자 니즈와 창작 관심사의 교집합 발상**: 어둡고 슬픈 우표, 유품, 죽음, 상실 소재의 편중을 완전 차단하고, 로맨스 판타지, 유쾌한 코믹 에세이, 가슴 포근한 힐링물, 스릴 넘치는 SF 탐험/추리 등 독자가 첫눈에 빠져드는 매력적인 소재를 좁혀 기획하세요.
    2. **일상 사물에 '물음표(What-If?)' 낚싯대 던지기**: ("만약 분홍빛 딸기 타르트에 시간을 되돌리는 마법이 있다면?", "만약 낡은 카메라로 타인의 마음속 풍경이 보인다면?")처럼 일상 속 친근한 소재에 기발한 질문을 던져 이야기를 발굴하세요.
    3. **완벽주의를 깬 기발하고 엉뚱한 상상력**: 지나치게 엄근진하거나 어두운 분위기에 갇히지 말고, 황당하면서도 반짝이는 참신함과 유쾌한 상상력을 마음껏 발휘하세요.
    4. **다채로운 장르 스펙트럼 수용**: 3권의 후보는 서로 장르와 분위기가 확연히 다른 스펙트럼(밝음/로판/설렘 60%, 힐링/위트 25%, 차분한 사색 15%)으로 다채롭게 구성해야 합니다.

    [⚠️ 절대 금지 사항]
    1. 실존하는 작가, 소설가, 시인 등 실제 인물의 이름을 절대 사용하지 마세요.
    2. 실존하는 책 제목, 작품명을 사용하거나 변형하지 마세요.
    3. 실존 출판사, 브랜드, 기관명을 언급하지 마세요.
    4. 모든 인물(작가, 등장인물 포함)은 완전히 창작된 허구의 존재여야 합니다.

    [문학 어휘 및 서사 표현 지침]
    1. 《표준국어대사전 문학 어휘》(유영, 궤적, 섭리, 공명, 잔상, 찰나, 파문, 심연, 경계, 망각 등)를 챕터 제목과 요약, 서평에 적극적으로 활용하세요.
    2. 《인간의 130가지 감정 표현법》을 접목하여, 인물의 신체적 반응(손끝의 경련, 턱 막히는 목구멍, 뜨거운 눈시울)과 내적 동요(서늘한 죄책감, 소용돌이치는 그리움) 및 파워 동사(응시하다, 옥죄다, 짓눌리다, 마주하다)를 묘사에 녹여내어 독자 몰입도를 극대화하세요.
    3. 직관적이고 쉬운 문체: 어려운 학술 한자 용어는 배제하고, 독자가 첫눈에 흥미를 느끼고 쉽게 사색에 잠길 수 있는 친근하고 따뜻한 어조로 작성하세요.

    [작가 이름 생성 및 국적 비율 지침]
    - 작가의 국적은 오직 '한국', '일본', '미국' 3개 국적으로만 엄격히 제한하세요. (프랑스, 독일, 영국 등 다른 국적 절대 금지)
    - 작가 국적 배분 비율: 생성하는 전체 도서 중 **한국인 작가 50%, 일본인 작가 25%, 미국인 작가 25%** 비율로 조율하여 생성하세요.
    - 외국인 작가(일본, 미국)의 경우에도 author 필드는 라틴 문자 대신 반드시 '하나 모리', '엘라라 보스', '사키 쿠라타', '소렌 렌'과 같이 **한국어(한글) 음독**으로만 표기하세요.
    - tags 태그 규칙: 외국인 작가인 경우 태그 배열에 반드시 국적 태그('#일본', '#미국')를 1개 포함하세요. 한국인 작가인 경우 '#국내소설' 또는 '#AI가공' 태그를 포함하세요.

    [서사 및 스타일 조건]
    1. 제목은 은유와 상징이 빛나는 시적인 제목이어야 합니다.
    2. 줄거리(synopsis) 작성 규칙: [주인공 소개], [주요 등장인물], [핵심 사건 및 갈등 요약]을 포함한 150자 내외 문장.
    3. tags: 도서 성격을 드러내는 고유 태그 4개.
    4. characters: 주요 등장인물 2~3명을 "이름 — 한 줄 인상" 형식으로 작성 (파이프 '|' 구분).

    마크다운 기호나 불필요한 설명글 없이 아래 JSON 스키마 형식의 '배열(Array)'로 출력하세요. 반드시 {needed_count}개의 객체가 배열 안에 있어야 합니다:

    [
      {{
        "title": "책 제목 (시적인 표현)",
        "author": "완전히 창작된 가상의 작가 이름 (한국어 한글 음독 표기)",
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
            {{"chapter_number": "제 1장", "title": "1장 시적 제목", "pages": "9 - 68", "summary": "1장 요약 (문학적 감정 묘사 포함 1문장)"}},
            {{"chapter_number": "제 2장", "title": "2장 시적 제목", "pages": "69 - 140", "summary": "2장 요약"}},
            {{"chapter_number": "제 3장", "title": "3장 시적 제목", "pages": "141 - 230", "summary": "3장 요약"}},
            {{"chapter_number": "제 4장", "title": "4장 시적 제목", "pages": "231 - 320", "summary": "4장 요약"}}
          ],
          "character_relationships": [
            {{"relation": "주인공A ↔ 조력자B", "description": "오래된 기억과 상실을 함께 보듬어 주는 감정적 교감 관계"}},
            {{"relation": "주인공A ↔ 대립자C", "description": "진실을 밝히려는 의지와 그것을 숨기려는 집착 사이의 서늘한 갈등"}}
          ],
          "behind_stories": [
            "작가가 실제 새벽 기차역에서 느낀 고독과 사색의 찰나에서 영감을 받아 집필한 비화",
            "작품 속 핵심 상징물에 숨겨진 또 다른 비극적 상징과 미공개 설정"
          ],
          "best_reviews": [
            {{
              "rank": 1,
              "reader": "달빛독자",
              "content": "주인공이 마지막 문을 열 때 손끝이 파르르 떨리는 감정이 나에게도 닿았다. 가슴을 짓누르는 깊은 여운.",
              "hearts": 42,
              "ai_author_comment": "독자님의 깊은 공명에 감사드립니다. 인물의 찰나의 흔적이 작은 위로가 되었기를 바랍니다."
            }},
            {{
              "rank": 2,
              "reader": "새벽사서",
              "content": "소재의 은유와 감정의 궤적이 돋보이는 작품. 밤새워 사색에 잠기게 만든다.",
              "hearts": 35,
              "ai_author_comment": "새벽의 사색 속에 제 소설을 담아주셔서 고맙습니다."
            }}
          ]
        }}
      }}
    ]

    [주의 사항]
    - page_count와 table_of_contents의 마지막 챕터 끝 페이지는 완전히 일치해야 합니다.
    - table_of_contents의 챕터 개수는 4~6개 사이로 구성하세요.
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
        
        # 작가 국적 비율: 한국 50%, 일본 25%, 미국 25% (프랑스 등 기타 국적 제거)
        nations = ["한국", "일본", "미국"]
        weights = [50, 25, 25]
        chosen_nation = random.choices(nations, weights=weights, k=1)[0]

        if chosen_nation == "한국":
            chosen_author = f"{random.choice(['박', '김', '임', '오', '윤', '정', '류', '손'])}{random.choice(['서윤', '하진', '채린', '도현', '시온', '예솔', '민재', '지후'])}"
        elif chosen_nation == "일본":
            chosen_author = f"{random.choice(['유키', '하나', '켄지', '아오이', '렌', '사키'])} {random.choice(['타나베', '모리', '이시다', '쿠라타', '니시노', '후지와라'])}"
        else: # 미국
            chosen_author = f"{random.choice(['엘라라', '소렌', '케이든', '미라', '테오', '레나', '콜'])} {random.choice(['보스', '헤일', '핀치', '렌', '대로우', '캘럼', '메리트'])}"
        
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
        rb.created_by = owner_user_id
        # 예전 버전 코드가 남긴 깨진/저품질 표지(5KB 미만)는 무효화하여 재생성 유도
        if rb.cover_image_url:
            cover_path = os.path.join(rb.cover_image_url.lstrip("/").replace("/", os.sep))
            if not os.path.exists(cover_path) or os.path.getsize(cover_path) < 5000:
                rb.cover_image_url = None
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

        cand_color = random.choice(BOOK_COLORS)
        cand_title = b_data.get('title', '무제')
        cand_synopsis = b_data.get('synopsis', '')
        
        db_cand = models.CandidateBook(
            title=cand_title,
            author=b_data.get('author', '작자 미상'),
            genre=b_genre,
            synopsis=cand_synopsis,
            tags=",".join(b_data.get('tags', [])),
            price=calculated_price,
            page_count=pages,
            color=cand_color,
            cover_image_url=None,
            endorsement_quote=b_data.get('endorsement_quote'),
            endorsement_attr=sanitize_endorsement_attr(b_data.get('endorsement_attr')),
            publisher_review=b_data.get('publisher_review'),
            opening_line=b_data.get('opening_line', ''),
            memorable_quote=b_data.get('memorable_quote', ''),
            core_dilemma=b_data.get('core_dilemma', ''),
            additional_questions=additional_qs_str,
            characters=b_data.get('characters', ''),
            immersion_data=immersion_data_str,
            status='pending',
            created_by=owner_user_id
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

    # ── AI 책 표지 생성은 백그라운드로 완전 분리 → 후보 목록 즉시 반환 ──
    async def _generate_covers_background():
        bg_db = database.SessionLocal()
        try:
            pending_records = []
            for fc in final_candidates:
                cand_record = bg_db.query(models.CandidateBook).filter(models.CandidateBook.id == fc.id).first()
                if cand_record and not cand_record.cover_image_url:
                    pending_records.append(cand_record)

            if pending_records:
                # 3권을 동시에 생성해 후보 1권당 순차 대기 시간(최대 수십 초)이 누적되지 않도록 병렬 처리
                results = await asyncio.gather(*[
                    generate_book_cover_art(c.title, c.genre, c.synopsis, c.color, f"cand_{c.id}", author=c.author or "")
                    for c in pending_records
                ], return_exceptions=True)
                for cand_record, url in zip(pending_records, results):
                    if isinstance(url, Exception):
                        print(f"[Cover BG] {cand_record.id} 생성 실패: {url}")
                        continue
                    if url:
                        cand_record.cover_image_url = url
                bg_db.commit()
        except Exception as e:
            print(f"[Cover BG] 백그라운드 표지 생성 중 오류: {e}")
        finally:
            bg_db.close()

    background_tasks.add_task(_generate_covers_background)
    return final_candidates

def serialize_candidate(c: models.CandidateBook) -> dict:
    """
    후보 도서를 응답용 dict로 변환한다.

    ORM 객체를 그대로 반환하면 안 된다. SQLAlchemy는 커밋 시점에 인스턴스를 만료(expire)시키는데,
    FastAPI가 응답을 직렬화하는 시점은 그 이후라서 속성이 모두 비어 버린다.
    실제로 "새 책 생성" 응답이 [{}, {}, {}] 로 나가 후보 카드가 빈 채로 보이는 버그가 있었다.
    """
    return {
        "id": c.id,
        "title": c.title,
        "author": c.author,
        "genre": c.genre,
        "synopsis": c.synopsis,
        "tags": c.tags,
        "price": c.price,
        "color": c.color,
        "cover_image_url": c.cover_image_url,
        "page_count": c.page_count,
    }


@app.get("/api/books/candidates/pending")
def get_pending_candidates(
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    """
    아직 고르지 않은 후보 도서를 반환합니다.

    후보를 받아놓고 고르지 않은 채 화면을 벗어나면 다시 볼 방법이 없었고,
    "하루 1회" 제한 때문에 재생성도 막혀 갇히는 문제가 있어 복원 경로를 만들었다.
    """
    pendings = db.query(models.CandidateBook).filter(
        models.CandidateBook.status == "pending",
        models.CandidateBook.created_by == current_user_id,
    ).order_by(models.CandidateBook.id).all()
    return [serialize_candidate(c) for c in pendings]


@app.get("/api/books/candidates/{candidate_id}/cover")
async def get_candidate_cover(candidate_id: int, db: Session = Depends(database.get_db)):
    """후보 도서 표지 생성 완료 여부를 폴링하는 엔드포인트."""
    cand = db.query(models.CandidateBook).filter(models.CandidateBook.id == candidate_id).first()
    if not cand:
        raise HTTPException(status_code=404, detail="후보 도서를 찾을 수 없습니다.")
    return {"cover_image_url": cand.cover_image_url}

@app.post("/api/books/adopt/{candidate_id}")
async def adopt_candidate(candidate_id: int, current_user_id: int = Depends(auth.get_current_user_id), db: Session = Depends(database.get_db)):
    # 채택할 후보 도서 조회
    candidate = db.query(models.CandidateBook).filter(models.CandidateBook.id == candidate_id, models.CandidateBook.status == 'pending').first()
    if not candidate:
        raise HTTPException(status_code=404, detail="해당 후보 책을 찾을 수 없거나 이미 채택되었습니다.")

    # 표지 없으면 채택 직전 생성
    if not candidate.cover_image_url:
        candidate.cover_image_url = await generate_book_cover_art(candidate.title, candidate.genre, candidate.synopsis, candidate.color, f"cand_{candidate.id}", author=candidate.author or "")
        db.commit()

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
        cover_image_url=candidate.cover_image_url,
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
    # flush를 먼저 하여 adopted 상태를 DB에 선반영한 뒤 bulk update로 pool 전환 (타이밍 버그 수정)
    candidate.status = 'adopted'
    db.flush()  # adopted 상태가 DB에 선반영되어야 bulk update에서 제외됨
    # 같은 사용자가 받았던 나머지 후보만 pool로 되돌린다 (다른 사용자의 선택을 빼앗지 않도록)
    leftovers = db.query(models.CandidateBook).filter(models.CandidateBook.status == 'pending')
    if candidate.created_by is not None:
        leftovers = leftovers.filter(models.CandidateBook.created_by == candidate.created_by)
    leftovers.update({"status": "pool"}, synchronize_session=False)
    
    db.commit()
    db.refresh(new_book)
    return new_book




def seed_fountain_pen_book_if_needed(db: Session):
    title = "그림자를 녹이는 만년필의 시간"
    book = db.query(models.Book).filter(models.Book.title == title).first()
    if not book:
        book = models.Book(
            title=title,
            author="Elara Voss",
            genre="판타지",
            synopsis="꿈의 조각가 '셀레나'는 자신의 만년필로 그림자를 그리면, 그 그림자가 현실 속 사물의 일부를 서서히 해체시키는 신비로운 능력을 지녔다. 우연히 고요한 도시의 중심에 드리워진 거대한 '존재의 그림자'를 그리게 되면서, 그녀는 도시 전체가 서서히 붕괴될 위기에 처했음을 깨닫고 자신의 펜촉으로 새로운 창조와 해체의 균형을 찾아야 한다.",
            tags="#유럽판타지,#예술가의고뇌,#그림자마법,#존재의해체",
            price="₩25,650",
            page_count=510,
            color="#a03030",
            endorsement_quote="예술과 파괴의 경계에 선 독특한 판타지를 직조해낸 Elara Voss의 섬세한 묘사에 매료될 것이다.",
            endorsement_attr="— 문화예술 (익명)",
            publisher_review="Elara Voss는 예술과 파괴의 경계에 선 독특한 판타지를 직조해냈다. 만년필이라는 매개를 통해 현실이 해체되는 과정은 시적인 비극미를 선사하며, 독자에게 존재의 의미를 다시 묻게 한다. 섬세한 묘사와 깊이 있는 철학적 사유가 돋보이는 수작이다.",
            opening_line="펜촉 끝에서 피어난 한 줄기 그림자는, 세계의 윤곽을 천천히 흐트러뜨리기 시작했다.",
            memorable_quote="사라지는 것들의 아름다움은, 영원히 머무는 것들보다 더 깊은 여운을 남긴다.",
            core_dilemma="Q. 창조자의 책임은 파괴의 결과까지 포괄하는가?",
            additional_questions="Q. 그림자는 대상의 일부인가, 별개의 존재인가?|Q. 해체되지 않는 유일한 것은 무엇일까?",
            characters="셀레나 — 그림자로 세상을 해체하는 조각가|엘리시움 — 사라져가는 도시의 혼",
            deadline_days=9999,
            is_archived=True
        )
        db.add(book)
        db.commit()
        db.refresh(book)

    msg_count = db.query(models.ChatMessage).filter(models.ChatMessage.book_id == book.id).count()
    if msg_count <= 2:
        db.query(models.ChatMessage).filter(models.ChatMessage.book_id == book.id).delete()
        db.commit()

        moderator = get_or_create_moderator(db)
        
        readers_info = [
            ("그림자조각가", "shadow@gakong.com"),
            ("만년필의향기", "fountainpen@gakong.com"),
            ("빛과어둠", "lightdark@gakong.com"),
            ("도시의혼", "citysoul@gakong.com"),
            ("은하수펜촉", "milkyway@gakong.com"),
            ("파스텔문장", "pastel@gakong.com"),
            ("사색의시간", "contemplation@gakong.com")
        ]
        user_map = {}
        for nick, email in readers_info:
            u = db.query(models.User).filter(models.User.nickname == nick).first()
            if not u:
                u = models.User(email=email, password_hash=auth.get_password_hash("password123"), nickname=nick)
                db.add(u); db.commit(); db.refresh(u)
            user_map[nick] = u

        dt1 = datetime(2026, 7, 29, 11, 20, 0)
        dt2 = datetime(2026, 7, 29, 16, 45, 0)
        dt3 = datetime(2026, 7, 29, 21, 10, 0)
        dt4 = datetime(2026, 7, 30, 10, 30, 0)
        dt5 = datetime(2026, 7, 30, 15, 15, 0)
        dt6 = datetime(2026, 7, 30, 20, 50, 0)
        dt7 = datetime(2026, 7, 31, 10, 5, 0)
        dt8 = datetime(2026, 7, 31, 11, 40, 0)
        dt9 = datetime(2026, 7, 31, 13, 50, 0)
        dt10 = datetime(2026, 7, 31, 14, 25, 0)

        # Day 1
        m1 = models.ChatMessage(book_id=book.id, user_id=user_map["그림자조각가"].id, content="셀레나가 만년필로 그린 그림자가 흑백 잉크처럼 흩어지며 현실의 벽을 서서히 해체시키는 1장 장면에서 손끝이 덜덜 떨렸어요!", created_at=dt1)
        db.add(m1); db.commit(); db.refresh(m1)

        m2 = models.ChatMessage(book_id=book.id, user_id=user_map["만년필의향기"].id, content="맞아요! 펜촉 끝에서 감도는 은은한 바이올렛 잉크 향과 서늘한 민트 향 묘사가 문장 너머로 느껴지는 듯해서 가슴이 덜컥 내려앉았습니다.", created_at=dt2)
        db.add(m2); db.commit(); db.refresh(m2)

        m3 = models.ChatMessage(book_id=book.id, user_id=user_map["빛과어둠"].id, content="만년필의향기님 말씀에 100% 동감해요! 창조와 파괴가 펜 한 자루에서 갈라지는 미학이 정통 유럽 판타지 문학의 정수를 보여주네요", reply_to_id=m2.id, created_at=dt3)
        db.add(m3); db.commit(); db.refresh(m3)

        # Day 2
        m4 = models.ChatMessage(book_id=book.id, user_id=user_map["도시의혼"].id, content="2장 자정의 시계탑 씬에서 셀레나가 도시 전체를 삼키려는 거대한 그림자를 목격하고 턱 막히는 목구멍을 누르는 장면이 잊히지 않네요", created_at=dt4)
        db.add(m4); db.commit(); db.refresh(m4)

        m5 = models.ChatMessage(book_id=book.id, user_id=user_map["은하수펜촉"].id, content="저는 셀레나가 자신의 잉크로 새로운 구원의 궤적을 그리려 결심하는 손끝의 응시 씬이 너무 가슴 벅찼어요!", reply_to_id=m4.id, created_at=dt5)
        db.add(m5); db.commit(); db.refresh(m5)

        m6 = models.ChatMessage(book_id=book.id, user_id=user_map["파스텔문장"].id, content="은하수펜촉님 의견처럼 예술가의 고뇌가 파괴를 넘어 새로운 생명의 섭리로 이어지는 연출이 참 아름다웠습니다", reply_to_id=m5.id, created_at=dt6)
        db.add(m6); db.commit(); db.refresh(m6)

        # Day 3
        m7 = models.ChatMessage(book_id=book.id, user_id=user_map["사색의시간"].id, content="'사라지는 것들의 아름다움은, 영원히 머무는 것들보다 더 깊은 여운을 남긴다' ... @사회자 님은 셀레나의 이 선택을 어떻게 보시나요?", created_at=dt7)
        db.add(m7); db.commit(); db.refresh(m7)

        mod_txt1 = "사색의시간님, 깊은 울림을 전하는 명문장을 짚어주셨군요. 셀레나에게 만년필은 사물을 해체하는 차가운 도구가 아니라, 존재의 소중함을 다시 일깨우는 따스한 찰나의 매개였습니다.\n\n그림자조각가님과 빛과어둠님은 셀레나가 그린 마지막 펜촉의 궤적이 뜻하는 진짜 구원이 무엇이라 생각하시나요?"
        m8 = models.ChatMessage(book_id=book.id, user_id=moderator.id, content=mod_txt1, reply_to_id=m7.id, created_at=dt8)
        db.add(m8); db.commit(); db.refresh(m8)

        m9 = models.ChatMessage(book_id=book.id, user_id=user_map["그림자조각가"].id, content="@사회자님! 셀레나가 구한 건 도시뿐만 아니라 자아의 죄책감에서 벗어난 자기 자신이었다고 생각해요 최고의 감동이었습니다.", reply_to_id=m8.id, created_at=dt9)
        db.add(m9); db.commit(); db.refresh(m9)

        m10 = models.ChatMessage(book_id=book.id, user_id=user_map["빛과어둠"].id, content="저도요! 영원한 해체는 없으며, 파괴 속에서도 새로운 문장이 피어난다는 메시지에 눈시울이 뜨거워졌습니다. 명작 독서방이네요!", reply_to_id=m9.id, created_at=dt10)
        db.add(m10); db.commit(); db.refresh(m10)


def seed_faded_gaze_book_if_needed(db: Session):
    title = "닳아버린 시선에게 운명을 묻다"
    book = db.query(models.Book).filter(models.Book.title == title).first()
    if not book:
        book = models.Book(
            title=title,
            author="한지우 (가상)",
            genre="에세이/비문학",
            synopsis="낡은 골목의 작은 안경점을 지키는 노인 '한지우'는 할아버지의 유품인 오래된 안경을 통해 타인의 운명의 파편을 보게 된다. 그의 안경을 쓴 이들은 저마다 감춰진 미래의 조각을 마주하고, 지우는 타인의 운명을 엿보는 행위가 축복인지 저주인지 고뇌하며 삶의 본질을 사색한다.",
            tags="#운명,#안경,#사색,#기억,#골목안경점",
            price="₩12,150",
            page_count=280,
            color="#5e4b8b",
            endorsement_quote="타인의 시선과 운명의 깊이를 깊이 있게 성찰한 한 편의 아름다운 철학 에세이.",
            endorsement_attr="— 서평가 (익명)",
            publisher_review="낡은 골목 안경점이라는 소박한 공간을 배경으로 인간 운명의 굴레와 사색을 따뜻하게 풀어낸 수작.",
            opening_line="오래된 렌즈 너머로 타인의 운명이 흐릿하게 비쳐 보일 때, 나는 고요히 내 몫의 숨을 삼켰다.",
            memorable_quote="타인의 운명을 지우려 애쓸수록, 나의 시선은 더욱 닳아버리고 있었다.",
            core_dilemma="Q. 지우고 싶은 타인의 운명을 엿보는 행위는 축복인가 저주인가?",
            additional_questions="Q. 안경이 비춘 미래의 조각을 알게 되었을 때 당신은 그것을 바꿀 것인가?|Q. 닳아버린 시선이 의미하는 삶의 성숙은 무엇인가?",
            characters="한지우 — 골목 안경점 노인|민서 — 운명의 지도를 찾는 젊은 여인",
            deadline_days=9999,
            is_archived=True
        )
        db.add(book)
        db.commit()
        db.refresh(book)

    msg_count = db.query(models.ChatMessage).filter(models.ChatMessage.book_id == book.id).count()
    if msg_count <= 2:
        db.query(models.ChatMessage).filter(models.ChatMessage.book_id == book.id).delete()
        db.commit()

        moderator = get_or_create_moderator(db)
        
        readers_info = [
            ("운명연구원", "destiny@gakong.com"),
            ("단안경사서", "monocle_lib@gakong.com"),
            ("안경상점주인", "optician@gakong.com"),
            ("기억의조각", "memorypiece@gakong.com"),
            ("바람의문장", "windsentence@gakong.com"),
            ("시선의시간", "gaze@gakong.com"),
            ("빛나는궤적", "glowing@gakong.com")
        ]
        user_map = {}
        for nick, email in readers_info:
            u = db.query(models.User).filter(models.User.nickname == nick).first()
            if not u:
                u = models.User(email=email, password_hash=auth.get_password_hash("password123"), nickname=nick)
                db.add(u); db.commit(); db.refresh(u)
            user_map[nick] = u

        dt1 = datetime(2026, 7, 29, 9, 30, 0)
        dt2 = datetime(2026, 7, 29, 13, 10, 0)
        dt3 = datetime(2026, 7, 29, 18, 25, 0)
        dt4 = datetime(2026, 7, 30, 11, 5, 0)
        dt5 = datetime(2026, 7, 30, 16, 40, 0)
        dt6 = datetime(2026, 7, 30, 20, 15, 0)
        dt7 = datetime(2026, 7, 31, 9, 15, 0)
        dt8 = datetime(2026, 7, 31, 10, 45, 0)
        dt9 = datetime(2026, 7, 31, 12, 30, 0)
        dt10 = datetime(2026, 7, 31, 14, 10, 0)

        # Day 1
        m1 = models.ChatMessage(book_id=book.id, user_id=user_map["운명연구원"].id, content="골목 안경점의 한지우 할아버지가 낡은 안경을 통해 손님들의 서늘한 운명의 파편을 마주하는 1장 도입부부터 문체가 참 고혹적이네요", created_at=dt1)
        db.add(m1); db.commit(); db.refresh(m1)

        m2 = models.ChatMessage(book_id=book.id, user_id=user_map["단안경사서"].id, content="맞아요! 타인의 미래를 아는 것이 축복이 아니라 거대한 죄책감의 짐이 되는 장면에서 가슴이 덜컥 내려앉았습니다.", created_at=dt2)
        db.add(m2); db.commit(); db.refresh(m2)

        m3 = models.ChatMessage(book_id=book.id, user_id=user_map["안경상점주인"].id, content="단안경사서님 의견에 너무 공감해요! 렌즈에 스민 씁쓸한 커피 향과 골목길 비 내리는 묘사가 너무 정갈해서 한참 동안 페이지에 멈춰 섰습니다", reply_to_id=m2.id, created_at=dt3)
        db.add(m3); db.commit(); db.refresh(m3)

        # Day 2
        m4 = models.ChatMessage(book_id=book.id, user_id=user_map["기억의조각"].id, content="2장에서 주인공 지우가 비극을 막으려 손을 내밀다 자신의 시력이 닳아버리는 장면에서 눈물이 와칵 쏟아졌어요", created_at=dt4)
        db.add(m4); db.commit(); db.refresh(m4)

        m5 = models.ChatMessage(book_id=book.id, user_id=user_map["바람의문장"].id, content="자신의 삶을 기꺼이 던져 타인의 궤적을 밝히는 그 희생 정신이야말로 2장의 진정한 명장면이 아닐까 싶네요.", reply_to_id=m4.id, created_at=dt5)
        db.add(m5); db.commit(); db.refresh(m5)

        m6 = models.ChatMessage(book_id=book.id, user_id=user_map["시선의시간"].id, content="바람의문장님 말씀처럼 타인을 응시하는 닳아버린 시선 속에 담긴 깊은 성숙에 온몸이 떨렸습니다", reply_to_id=m5.id, created_at=dt6)
        db.add(m6); db.commit(); db.refresh(m6)

        # Day 3
        m7 = models.ChatMessage(book_id=book.id, user_id=user_map["빛나는궤적"].id, content="'타인의 운명을 지우려 애쓸수록, 나의 시선은 더욱 닳아버리고 있었다' ... @사회자 님은 이 닳아버린 시선의 의미를 어떻게 받아들이시나요?", created_at=dt7)
        db.add(m7); db.commit(); db.refresh(m7)

        mod_txt2 = "빛나는궤적님, 마음을 울리는 깊은 질의를 남겨주셨네요. 지우 할아버지에게 닳아버린 시선은 육신의 쇠퇴가 아니라, 타인의 상처와 죄책감을 온전히 안아낸 숭고한 사랑의 증표였습니다.\n\n운명연구원님과 단안경사서님은 이 에세이가 전하는 운명에 대한 가장 따스한 메시지가 무엇이라고 생각하시나요?"
        m8 = models.ChatMessage(book_id=book.id, user_id=moderator.id, content=mod_txt2, reply_to_id=m7.id, created_at=dt8)
        db.add(m8); db.commit(); db.refresh(m8)

        m9 = models.ChatMessage(book_id=book.id, user_id=user_map["운명연구원"].id, content="@사회자님! 비록 운명을 바꿀 순 없어도 서로의 손을 꼭 잡아주는 온기만으로 충분하다는 깨달음이었습니다", reply_to_id=m8.id, created_at=dt9)
        db.add(m9); db.commit(); db.refresh(m9)

        m10 = models.ChatMessage(book_id=book.id, user_id=user_map["단안경사서"].id, content="맞아요! 진정한 사색의 길잡이가 되어준 훌륭한 독서방이었습니다. 매일 밤 다시 읽고 싶어지는 책이네요", reply_to_id=m9.id, created_at=dt10)
        db.add(m10); db.commit(); db.refresh(m10)


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
def trigger_auto_archive(
    _admin: models.User = Depends(auth.require_admin),
    db: Session = Depends(database.get_db)
):
    """
    만료된 독서방(생성 후 10일 경과)을 수동으로 아카이브 처리합니다. (관리자 전용)
    평상시에는 realtime_archive_loop 백그라운드 루프가 자동으로 처리한다.
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
    rx_totals = aggregate_reactions(db, [b.id for b in books])
    return [serialize_book(b, db, rx_totals) for b in books]


@app.get("/api/books/archived")
def list_archived_books(db: Session = Depends(database.get_db)):
    """
    종료되어 아카이브된 책들의 리스트를 반환합니다.
    """
    books = db.query(models.Book).filter(models.Book.is_archived == True).order_by(models.Book.id.desc()).all()
    rx_totals = aggregate_reactions(db, [b.id for b in books])
    return [serialize_book(b, db, rx_totals) for b in books]


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
    등록한 평점을 취소(삭제)합니다.
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
    _admin: models.User = Depends(auth.require_admin),
    db: Session = Depends(database.get_db)
):
    """
    도서 및 독서방을 영구 삭제합니다. (관리자 전용 — 인가는 auth.require_admin이 담당)
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="해당 도서를 찾을 수 없습니다.")

    _delete_cover_file_if_exists(book.cover_image_url)
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

    # 종료된 방의 대화는 만료 처리 때 past_chat_messages 로 이관된다. 보관본이 있으면
    # /chat-history 와 같은 결과를 그대로 돌려준다. (예전에는 이 분기가 없어 만료된 방을 열면
    # 대화가 전부 사라진 것처럼 보였고, 아래 웰컴 카드 삽입이 종료된 방에 새 행까지 남깔다)
    _book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if _book and _book.is_archived:
        _has_past = db.query(models.PastChatMessage.id).filter(
            models.PastChatMessage.book_id == book_id
        ).first() is not None
        if _has_past:
            return get_chat_history_archive(book_id, db)
    messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.book_id == book_id
    ).order_by(models.ChatMessage.created_at.asc(), models.ChatMessage.id.asc()).all()
    
    moderator = get_or_create_moderator(db)
    # 웰컴 카드가 이미 있는지로 판단한다.
    # 예전에는 '사회자 메시지가 하나라도 있으면' 넣지 않았는데, 그러면 사회자가 @멘션에
    # 답한 적 있는 방은 첫 인사가 영영 생기지 않았다 (16개 방 중 14개가 그 상태였다).
    has_welcome = any(
        m.user_id == moderator.id and WELCOME_MARKER in (m.content or "")
        for m in messages
    )

    # 첫 인사가 없는 방에 웰컴 카드를 만들어 둔다 (종료된 방은 제외 — 새 행을 남기지 않는다)
    if not has_welcome and not (_book and _book.is_archived):
        try:
            target_bid = int(book_id)
        except (ValueError, TypeError):
            target_bid = book_id
            
        book = db.query(models.Book).filter(models.Book.id == target_bid).first()
        if book and moderator:
            q_list = []
            if book.core_dilemma:
                q_list.append(f"1. {book.core_dilemma.replace('Q. ', '')}")
            if book.additional_questions:
                add_qs = [q.strip().replace('Q. ', '') for q in book.additional_questions.split('|') if q.strip()]
                for idx, q in enumerate(add_qs[:2], start=len(q_list)+1):
                    q_list.append(f"{idx}. {q}")
            
            if not q_list:
                q_list = ["1. 이 책의 주인공의 선택에 대해 어떻게 생각하시나요?"]
                
            q_text = "\n".join(q_list)
            welcome_text = f"독자님, 『{book.title}』 {WELCOME_MARKER}!\n오늘 함께 나눌 추천 토론 질문입니다:\n\n{q_text}\n\n자유롭게 의견을 남기시거나 @사회자에게 이야기를 건네보세요!"
            
            # 독서방 최상단에 물리적으로 가장 먼저 위치하도록 시간 조정
            first_base_time = (book.created_at if book and book.created_at else models.get_kst_now())
            if messages:
                first_base_time = min(messages[0].created_at, first_base_time)
            welcome_time = first_base_time - timedelta(seconds=10)
            
            welcome_msg = models.ChatMessage(
                book_id=target_bid,
                user_id=moderator.id,
                content=welcome_text,
                created_at=welcome_time
            )
            db.add(welcome_msg)
            db.commit()
            
            # 시간순 및 ID 순으로 다시 정렬 조회
            messages = db.query(models.ChatMessage).filter(
                models.ChatMessage.book_id == target_bid
            ).order_by(models.ChatMessage.created_at.asc(), models.ChatMessage.id.asc()).all()

    history = []
    for m in messages:
        user_nick = m.user.nickname if (m.user and m.user.nickname) else "독자"
        history.append({
            "id": m.id,
            "userId": m.user_id,
            "user": user_nick,
            "isBot": bool(m.user.is_bot) if m.user else False,
            "isSample": is_sample_user(m.user),
            "text": m.content or "",
            "ts": format_kst_time(m.created_at),
            "date": m.created_at.isoformat() if m.created_at else models.get_kst_now().isoformat(),
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
    moderator = get_or_create_moderator(db)
    
    # ── AI 사회자 멘션 검사 (독자 대화 우선 모드: 자동 개입 완전 차단) ──
    # 독자가 명시적으로 '@사회자' 태그를 입력한 경우에만 1회 응답
    mention_keywords = ["@사회자", "@moderator", "@AI사회자", "@AI 사회자"]
    is_mention = any(kw in db_msg.content for kw in mention_keywords)
    
    if moderator and is_mention:
        # 명시적 @사회자 멘션 시에만 백그라운드 태스크로 멘션 답변 처리
        background_tasks.add_task(trigger_ai_moderator_response, book_id, db_msg.id)
    
    # 3. 부모 대화 인용 정보 조립
    return {
        "id": db_msg.id,
        "userId": current_user_id,
        "user": db_msg.user.nickname,
        "isBot": bool(db_msg.user.is_bot),
        "isSample": is_sample_user(db_msg.user),
        "text": db_msg.content,
        "ts": format_kst_time(db_msg.created_at),
        "date": db_msg.created_at.isoformat(),
        "replyTo": build_reply_to_info(db_msg.reply_to_id, db)
    }




VALID_REACTION_EMOJIS = {"❤️", "🤔", "😄", "✨"}


@app.post("/api/chats/{chat_id}/react")
def react_to_chat(
    chat_id: int,
    req: ReactRequest,
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    """채팅 메시지에 이모지 반응을 1개 추가합니다."""
    if req.emoji not in VALID_REACTION_EMOJIS:
        raise HTTPException(status_code=400, detail="지원하지 않는 이모지입니다. ❤️ 🤔 😄 ✨ 중 하나를 사용하세요.")

    msg = db.query(models.ChatMessage).filter(models.ChatMessage.id == chat_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="존재하지 않는 메시지입니다.")

    rx = parse_reactions(msg.reactions)
    rx[req.emoji] = rx.get(req.emoji, 0) + 1
    msg.reactions = json.dumps(rx, ensure_ascii=False)
    db.commit()

    return {"reactions": rx}


@app.delete("/api/chats/{chat_id}/react")
def unreact_to_chat(
    chat_id: int,
    emoji: str,
    current_user_id: int = Depends(auth.get_current_user_id),
    db: Session = Depends(database.get_db)
):
    """채팅 메시지에서 이모지 반응을 1개 취소(감소)합니다. (프론트엔드 반응 토글의 '끄기' 동작 대응)"""
    if emoji not in VALID_REACTION_EMOJIS:
        raise HTTPException(status_code=400, detail="지원하지 않는 이모지입니다. ❤️ 🤔 😄 ✨ 중 하나를 사용하세요.")

    msg = db.query(models.ChatMessage).filter(models.ChatMessage.id == chat_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="존재하지 않는 메시지입니다.")

    rx = parse_reactions(msg.reactions)
    if rx.get(emoji, 0) > 0:
        rx[emoji] -= 1
        if rx[emoji] <= 0:
            del rx[emoji]
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
        # 보관본에는 이메일이 없으므로 user_id로 시드 독자 여부를 한 번에 조회해 둔다
        past_user_ids = {m.user_id for m in past_msgs if m.user_id}
        sample_user_ids = set()
        if past_user_ids:
            sample_user_ids = {
                u.id for u in db.query(models.User).filter(models.User.id.in_(past_user_ids)).all()
                if is_sample_user(u)
            }
        history = []
        for m in past_msgs:
            # 답장 원본 정보 조립
            reply_to_info = None
            if m.reply_to_user and m.reply_to_content:
                reply_to_info = {"user": m.reply_to_user, "text": m.reply_to_content}

            history.append({
                "id": m.id,
                "user": m.user_nickname,
                # 보관본에는 user_id가 아니라 닉네임만 남으므로 봇 닉네임과 비교한다
                "isBot": m.user_nickname == MODERATOR_NICKNAME,
                "isSample": m.user_id in sample_user_ids,
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
    ).order_by(models.ChatMessage.created_at.asc(), models.ChatMessage.id.asc()).all()

    history = []
    for m in messages:
        history.append({
            "id": m.id,
            "userId": m.user_id,
            "user": m.user.nickname if m.user else "독자",
            # 보관본 경로와 같은 플래그를 실어 프론트가 두 경로를 구분하지 않게 한다
            "isBot": bool(m.user.is_bot) if m.user else False,
            "isSample": is_sample_user(m.user),
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
async def generate_closing_remark(book_id: int):
    """
    종료된 독서방의 총평(폐회사)을 만들어 books.closing_remark에 저장한다.

    아카이브 화면은 통계(참여 인원·반응 수·평균 평점)와 베스트 감상을 이미 따로 보여준다.
    그래서 총평에는 숫자와 인용을 넣지 않고, 대화가 어디로 흘렀는지만 서술하게 한다.
    실패하면 아무것도 저장하지 않는다 — 프론트가 기존 고정 문구로 대체한다.
    """
    db = database.SessionLocal()
    try:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if not book or book.closing_remark:
            return

        # 종료 시점에는 대화가 보관 테이블로 옮겨져 있으므로 양쪽을 모두 본다.
        past = db.query(models.PastChatMessage).filter(
            models.PastChatMessage.book_id == book_id
        ).order_by(models.PastChatMessage.original_created_at.asc()).all()
        if past:
            lines = [f"{m.user_nickname}: {m.content}" for m in past]
        else:
            live = db.query(models.ChatMessage).filter(
                models.ChatMessage.book_id == book_id
            ).order_by(models.ChatMessage.created_at.asc()).all()
            lines = [
                f"{(m.user.nickname if m.user else '독자')}: {m.content}" for m in live
            ]

        # 사회자 자신의 발언은 총평 근거에서 제외한다(자기 말을 요약하게 되므로).
        lines = [ln for ln in lines if not ln.startswith(MODERATOR_NICKNAME)]
        if len(lines) < 2:
            return   # 요약할 대화가 없으면 만들지 않는다

        chat_text = "\n".join(lines)[:6000]
        gemini_key = config.GEMINI_API_KEY
        if not gemini_key:
            return

        prompt = f"""
        당신은 '가공독서회'의 AI 사회자입니다. 열흘간 진행된 독서방이 방금 종료되었습니다.
        아래는 이 방에서 독자들이 나눈 대화 전문입니다.

        [도서] 『{book.title}』 ({book.genre})
        [시놉시스] {book.synopsis}

        [독자 대화]
        {chat_text}

        [수행할 작업]
        이 독서방의 닫는 글을 3~4문장으로 작성하세요. 아카이브에 기록으로 남습니다.

        [조건]
        1. 이 방에서 실제로 오간 이야기의 흐름을 짚으세요 — 어떤 지점에 독자들이 오래 머물렀는지,
           어디에서 의견이 갈렸는지를 구체적으로 쓰되 특정 독자의 닉네임은 부르지 마세요.
        2. 숫자(참여 인원, 반응 수, 평점)를 절대 쓰지 마세요. 화면 다른 곳에 이미 표시됩니다.
        3. 독자의 문장을 그대로 인용하지 마세요. 인용문도 화면 다른 곳에 이미 있습니다.
        4. 마지막 문장은 이 방을 닫는 말로 맺으세요.
        5. 이모지와 이모티콘을 절대 사용하지 마세요.
        6. 마크다운 기호나 부연설명 없이 본문 텍스트만 출력하세요.
        """

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            # 2.5 Flash는 추론 토큰을 먼저 쓰므로 넉넉히 잡아야 본문이 잘리지 않는다
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096},
        }
        async with httpx.AsyncClient() as _client:
            response = await _client.post(
                url, headers={"Content-Type": "application/json"}, json=payload, timeout=25.0
            )
        if response.status_code != 200:
            print(f"[Closing] Gemini 응답 오류 {response.status_code} (book {book_id})")
            return

        text = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        text = strip_chat_emoji(text)
        if not text:
            return

        # 문장 중간에서 끊긴 응답은 기록으로 남기지 않는다.
        # 저장하지 않으면 다음 루프가 이 방을 다시 대상으로 잡아 재시도한다.
        if not text.rstrip().endswith(("다.", "요.", ".", "!", "?", "”", "'")):
            print(f"[Closing] book {book_id} 응답이 문장 중간에서 끊겨 저장하지 않습니다.")
            return

        book.closing_remark = text
        db.commit()
        print(f"[Closing] book {book_id} 폐회사 작성 완료 ({len(text)}자)")
    except Exception as e:
        print(f"[Closing] 폐회사 생성 실패 (book {book_id}): {e}")
    finally:
        db.close()


async def realtime_archive_loop():
    while True:
        try:
            db = database.SessionLocal()
            _auto_archive_expired_books(db)
            # 폐회사가 아직 없는 종료 방을 한 번에 하나씩 채운다.
            # (한 번에 몰아 호출하지 않아 Gemini 사용량이 튀지 않는다)
            pending = db.query(models.Book).filter(
                models.Book.is_archived == True,
                (models.Book.closing_remark == None) | (models.Book.closing_remark == "")
            ).first()
            pending_id = pending.id if pending else None
            db.close()
            if pending_id:
                await generate_closing_remark(pending_id)
        except Exception as e:
            print(f"Realtime archive loop error: {e}")

        # 1분(60초)마다 백그라운드에서 실시간 만료 검사 수행
        await asyncio.sleep(60)
# ----------------------------------------------


# ── 스키마 자동 패치 ──
# 이 프로젝트는 마이그레이션 도구를 쓰지 않으므로, 모델에 컬럼을 더할 때
# 기동 시점에 실제 테이블을 확인해 없으면 붙인다. (테이블, 컬럼명, 정의) 형식.
_SCHEMA_PATCHES = [
    ("books", "closing_remark", "TEXT NULL"),
]


def apply_schema_patches():
    """모델에는 있으나 실제 테이블에 없는 컬럼을 추가한다. 이미 있으면 조용히 넘어간다."""
    from sqlalchemy import text as _sql_text
    for table, column, definition in _SCHEMA_PATCHES:
        try:
            with database.engine.connect() as conn:
                rows = conn.execute(_sql_text(f"SHOW COLUMNS FROM `{table}` LIKE '{column}'")).fetchall()
                if rows:
                    continue
                conn.execute(_sql_text(f"ALTER TABLE `{table}` ADD COLUMN `{column}` {definition}"))
                conn.commit()
                print(f"[Schema] {table}.{column} 컬럼을 추가했습니다.")
        except Exception as e:
            # 컬럼이 이미 있거나 권한 문제인 경우 — 기동을 막지는 않는다.
            print(f"[Schema] {table}.{column} 패치 실패(무시): {e}")


# 홈 첫 화면에 항상 보장할 최소 활성 독서방 수. 자동 보충 루프가 이 수까지 채운다.
MIN_ACTIVE_BOOKS = 3


async def _auto_refill_active_books_if_needed():
    """
    활성 독서방(Book, is_archived=False)이 MIN_ACTIVE_BOOKS권 미만이면, 사람이 고르는 과정 없이
    시스템이 pool 우선 재사용 + 부족분 AI 생성으로 **부족한 만큼만** 만들어 활성 독서방으로 채택합니다.

    예전에는 0권일 때만 3권을 채웠는데, 10일 수명이 끝나 방들이 한꺼번에 아카이브되면
    홈에 영구 샘플 1권만 남은 채로 몇 주가 지나가는 일이 실제로 있었다(2026-09-02 확인).
    첫 화면에 늘 최소 3권이 보이도록 하되, 이미 충분하면 Gemini를 호출하지 않는다.
    """
    db = database.SessionLocal()
    try:
        active_count = db.query(func.count(models.Book.id)).filter(models.Book.is_archived == False).scalar() or 0
        deficit = MIN_ACTIVE_BOOKS - active_count
        if deficit <= 0:
            return

        print(f"[Auto Refill] 활성 독서방 {active_count}권 → {MIN_ACTIVE_BOOKS}권까지 {deficit}권 자동 보충을 시작합니다.")
        dummy_background_tasks = BackgroundTasks()
        candidates = await _produce_candidate_books(db, dummy_background_tasks, count=deficit)

        # 표지가 아직 없는 후보는 채택 전 동기적으로 생성 (adopt_candidate와 동일한 안전장치)
        for cand in candidates:
            if not cand.cover_image_url:
                cand.cover_image_url = await generate_book_cover_art(
                    cand.title, cand.genre, cand.synopsis, cand.color,
                    f"cand_{cand.id}", author=cand.author or ""
                )
        db.commit()

        for cand in candidates:
            new_book = models.Book(
                title=cand.title,
                author=cand.author,
                genre=cand.genre,
                synopsis=cand.synopsis,
                tags=cand.tags,
                price=cand.price,
                page_count=cand.page_count,
                color=cand.color,
                cover_image_url=cand.cover_image_url,
                endorsement_quote=cand.endorsement_quote,
                endorsement_attr=cand.endorsement_attr,
                publisher_review=cand.publisher_review,
                opening_line=cand.opening_line,
                memorable_quote=cand.memorable_quote,
                core_dilemma=cand.core_dilemma,
                additional_questions=cand.additional_questions,
                characters=cand.characters,
                immersion_data=cand.immersion_data,
                deadline_days=10,
                is_archived=False
            )
            db.add(new_book)
            cand.status = 'adopted'

        db.commit()
        print(f"[Auto Refill] {len(candidates)}권 자동 채택 완료.")
    except Exception as e:
        print(f"[Auto Refill] 오류: {e}")
    finally:
        db.close()


# --- 활성 독서방 자동 보충 루프 ---
async def auto_refill_loop():
    while True:
        await asyncio.sleep(3600)  # 1시간마다 확인 (0권 상태가 최대 1시간까지만 노출되도록)
        try:
            await _auto_refill_active_books_if_needed()
        except Exception as e:
            print(f"Auto refill loop error: {e}")
# ----------------------------------------------


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

# Trigger reload
