import os
import json
import asyncio
import random
import secrets
import string
import base64
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

import database
import models
import auth

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


def _hex_to_rgb(h: str):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def _draw_gradient_bg(img, colors, mode="diagonal"):
    """배경 그라데이션: diagonal / radial / horizontal / vertical"""
    from PIL import Image
    W, H = img.size
    px = img.load()
    c1, c2 = colors[0], colors[1]
    c3 = colors[2] if len(colors) > 2 else c2
    if mode == "horizontal":
        for y in range(H):
            t = y / H
            ca = _lerp_color(c1, c2, min(t * 1.8, 1.0))
            cb = _lerp_color(c2, c3, max(0, t * 1.8 - 0.8))
            col = _lerp_color(ca, cb, t)
            for x in range(W):
                px[x, y] = col
    elif mode == "radial":
        cx, cy = W // 2, H // 2
        maxd = ((cx**2 + cy**2) ** 0.5)
        for y in range(H):
            for x in range(W):
                d = ((x - cx)**2 + (y - cy)**2) ** 0.5
                t = min(d / maxd, 1.0)
                px[x, y] = _lerp_color(c1, c2, t)
    elif mode == "diagonal":
        for y in range(H):
            for x in range(W):
                t = (x / W * 0.4 + y / H * 0.6)
                t = min(t, 1.0)
                px[x, y] = _lerp_color(c1, c2, t)
    else:  # vertical
        for y in range(H):
            for x in range(W):
                t = (x / W * 0.6 + y / H * 0.4)
                t = min(t, 1.0)
                px[x, y] = _lerp_color(c1, c2, t)
    return img

def _analyze_book(genre: str, synopsis: str, title: str):
    """줄거리·장르·제목에서 시각 무드 키워드를 분석하여 팔레트·구도를 결정"""
    text = (genre + " " + title + " " + synopsis).lower()
    # ── 감정/소재 키워드 탐지 ──
    is_dark    = any(k in text for k in ["죽음","살인","어둠","공포","밤","악","괴물","범죄","사체","흑","암흑"])
    is_warm    = any(k in text for k in ["사랑","따뜻","봄","꽃","설레","연인","마음","행복","포근"])
    is_nature  = any(k in text for k in ["숲","나무","자연","바다","강","식물","새","바람","구름","산"])
    is_cold    = any(k in text for k in ["겨울","눈","차갑","얼음","서리","냉","한랭","북위"])
    is_tension = any(k in text for k in ["추격","위협","탈출","긴장","전쟁","싸움","폭발","음모"])
    is_mystic  = any(k in text for k in ["마법","신비","환상","용","마녀","예언","전설","이계"])
    is_urban   = any(k in text for k in ["도시","서울","도쿄","거리","건물","카페","아파트","회사"])
    is_scifi   = any(k in text for k in ["우주","로봇","미래","ai","인공지능","사이버","행성","우주선"])

    # ── 장르 오버라이드 ──
    g = genre.lower()
    if "sf" in g or "공상" in g: is_scifi = True
    if "공포" in g or "호러" in g: is_dark = True
    if "로맨스" in g: is_warm = True
    if "미스터리" in g or "스릴러" in g: is_tension = True
    if "판타지" in g: is_mystic = True
    if "역사" in g: is_warm = False

    return {
        "dark": is_dark, "warm": is_warm, "nature": is_nature,
        "cold": is_cold, "tension": is_tension, "mystic": is_mystic,
        "urban": is_urban, "scifi": is_scifi
    }

def _pick_palette(mood: dict, base_color: tuple):
    """무드에 따라 3-4색 팔레트를 반환"""
    if mood["scifi"]:
        return [(8, 10, 30), (0, 180, 220), (100, 30, 160), (0, 255, 200)]
    if mood["dark"] and mood["tension"]:
        return [(10, 5, 20), (120, 0, 30), (60, 0, 80), (200, 20, 50)]
    if mood["dark"]:
        return [(15, 10, 25), (70, 0, 90), (30, 20, 60), (180, 140, 60)]
    if mood["mystic"]:
        return [(20, 0, 60), (100, 0, 180), (200, 150, 0), (60, 0, 120)]
    if mood["cold"]:
        return [(200, 230, 255), (100, 160, 220), (30, 80, 160), (220, 240, 255)]
    if mood["nature"]:
        return [(30, 80, 40), (80, 160, 60), (200, 220, 100), (240, 200, 80)]
    if mood["warm"]:
        return [(255, 200, 180), (220, 80, 100), (255, 140, 60), (180, 40, 80)]
    if mood["urban"]:
        return [(20, 20, 35), (50, 80, 140), (200, 200, 220), (80, 120, 180)]
    if mood["tension"]:
        return [(20, 10, 10), (180, 40, 0), (240, 160, 0), (100, 20, 20)]
    # 기본: base_color 중심
    r, g, b = base_color
    return [
        (max(r-80,0), max(g-80,0), max(b-80,0)),
        base_color,
        (min(r+60,255), min(g+40,255), min(b+80,255)),
        (min(r+120,255), min(g+100,255), max(b-40,0))
    ]

def _pick_composition(mood: dict, rng) -> str:
    """무드에 따라 구도 스타일 반환"""
    if mood["scifi"] or mood["urban"]:
        return rng.choice(["grid", "circuit", "hexagon"])
    if mood["mystic"]:
        return rng.choice(["radial_burst", "spiral", "concentric"])
    if mood["tension"] or mood["dark"]:
        return rng.choice(["diagonal_shards", "sharp_layers", "triangles"])
    if mood["warm"] or mood["nature"]:
        return rng.choice(["soft_circles", "waves", "petals"])
    if mood["cold"]:
        return rng.choice(["crystal", "sharp_layers", "concentric"])
    return rng.choice(["geometric_mix", "diagonal_shards", "soft_circles", "radial_burst"])

def _generate_abstract_cover_pil(title: str, genre: str, synopsis: str, base_color_hex: str, filepath: str):
    """PIL로 책 내용 기반 추상 기하학 표지를 생성"""
    import hashlib
    import math
    from PIL import Image, ImageDraw, ImageFilter

    W, H = 450, 600

    # 결정론적 시드: 같은 책은 항상 같은 표지
    seed_val = int(hashlib.md5((title + genre).encode('utf-8', errors='ignore')).hexdigest()[:8], 16)
    rng = random.Random(seed_val)

    base_rgb = _hex_to_rgb(base_color_hex) if base_color_hex and len(base_color_hex) >= 6 else (120, 80, 160)
    mood = _analyze_book(genre, synopsis, title)
    palette = _pick_palette(mood, base_rgb)
    composition = _pick_composition(mood, rng)

    # ── 배경 그라데이션 ──
    bg_modes = {"dark": "horizontal", "mystic": "radial", "warm": "diagonal",
                "scifi": "horizontal", "cold": "vertical", "tension": "diagonal"}
    bg_mode = next((bg_modes[k] for k in bg_modes if mood.get(k)), "diagonal")
    img = Image.new('RGB', (W, H), palette[0])
    img = _draw_gradient_bg(img, [palette[0], palette[1], palette[2] if len(palette)>2 else palette[1]], bg_mode)

    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    def rand_color(alpha=None):
        c = rng.choice(palette)
        a = alpha if alpha is not None else rng.randint(80, 200)
        return (*c, a)

    # ── 구도별 도형 배치 ──
    if composition == "grid":
        # SF/도시: 격자 + 직사각형 블록
        cell = rng.randint(40, 80)
        for gy in range(0, H, cell):
            for gx in range(0, W, cell):
                if rng.random() < 0.35:
                    bw = rng.randint(cell//3, cell)
                    bh = rng.randint(cell//3, cell)
                    c = rand_color(rng.randint(60, 160))
                    draw.rectangle([gx, gy, gx+bw, gy+bh], fill=c)
        # 밝은 선 격자
        line_c = (*palette[-1], 40)
        for gx in range(0, W, cell):
            draw.line([(gx,0),(gx,H)], fill=line_c, width=1)
        for gy in range(0, H, cell):
            draw.line([(0,gy),(W,gy)], fill=line_c, width=1)

    elif composition == "circuit":
        # 회로 패턴
        for _ in range(18):
            x1, y1 = rng.randint(0,W), rng.randint(0,H)
            seg_len = rng.randint(30, 120)
            direction = rng.choice(['h','v'])
            x2 = (x1 + seg_len) if direction == 'h' else x1
            y2 = y1 if direction == 'h' else (y1 + seg_len)
            c = (*rng.choice(palette), rng.randint(100, 200))
            draw.line([(x1,y1),(x2,y2)], fill=c, width=rng.randint(1,3))
            # 노드
            r = rng.randint(3,8)
            draw.ellipse([x2-r,y2-r,x2+r,y2+r], fill=(*palette[-1], 180))

    elif composition == "hexagon":
        # 육각형 그리드
        size = rng.randint(35, 60)
        for row in range(-1, H // size + 2):
            for col in range(-1, W // size + 2):
                cx = col * size * 1.73 + (size * 0.87 if row % 2 else 0)
                cy = row * size * 1.5
                pts = []
                for angle in range(0, 360, 60):
                    rad = math.radians(angle)
                    pts.append((cx + size * 0.9 * math.cos(rad), cy + size * 0.9 * math.sin(rad)))
                if rng.random() < 0.6:
                    c = rand_color(rng.randint(40, 150))
                    draw.polygon(pts, fill=c)

    elif composition == "radial_burst":
        # 방사형 폭발: 중심에서 퍼지는 삼각형들
        cx, cy = W // 2, rng.randint(H//3, 2*H//3)
        for i in range(rng.randint(12, 20)):
            angle = i * (360 / 18) + rng.uniform(-8, 8)
            r_in  = rng.randint(20, 80)
            r_out = rng.randint(120, 280)
            a1 = math.radians(angle - 8)
            a2 = math.radians(angle + 8)
            pts = [
                (cx + r_in * math.cos(a1),  cy + r_in * math.sin(a1)),
                (cx + r_out * math.cos(a1), cy + r_out * math.sin(a1)),
                (cx + r_out * math.cos(a2), cy + r_out * math.sin(a2)),
                (cx + r_in * math.cos(a2),  cy + r_in * math.sin(a2)),
            ]
            c = rand_color(rng.randint(60, 160))
            draw.polygon(pts, fill=c)

    elif composition == "spiral":
        # 나선형 점들
        cx, cy = W//2, H//2
        for i in range(200):
            t = i / 200 * 6 * math.pi
            r = 10 + 100 * (i / 200)
            x = cx + r * math.cos(t)
            y = cy + r * math.sin(t) * 1.3
            dot = rng.randint(2, 8)
            c = rand_color(rng.randint(100, 220))
            draw.ellipse([x-dot, y-dot, x+dot, y+dot], fill=c)

    elif composition == "concentric":
        # 동심원
        cx, cy = rng.randint(W//3, 2*W//3), rng.randint(H//3, 2*H//3)
        for i in range(rng.randint(8, 15)):
            r = 30 + i * rng.randint(20, 35)
            c = rand_color(rng.randint(40, 140))
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=c, width=rng.randint(2, 8))

    elif composition == "diagonal_shards":
        # 대각선 파편: 다각형 조각
        for _ in range(rng.randint(8, 16)):
            x  = rng.randint(-50, W)
            y  = rng.randint(-50, H)
            pts = [(x + rng.randint(-80,80), y + rng.randint(-100,100)) for _ in range(rng.randint(3,6))]
            c = rand_color(rng.randint(60, 180))
            draw.polygon(pts, fill=c)

    elif composition == "sharp_layers":
        # 날카로운 레이어: 가로 사다리꼴들
        for i in range(rng.randint(6, 11)):
            y  = i * (H // 9)
            skew = rng.randint(-60, 60)
            pts = [(0, y), (W, y + skew), (W, y + skew + rng.randint(30,80)), (0, y + rng.randint(30,80))]
            c = rand_color(rng.randint(50, 160))
            draw.polygon(pts, fill=c)

    elif composition == "triangles":
        # 삼각형 타일
        size = rng.randint(60, 120)
        for row in range(-1, H // size + 2):
            for col in range(-1, W // size + 2):
                x, y = col * size, row * size
                # 위 삼각형
                pts1 = [(x, y+size), (x+size, y+size), (x+size//2, y)]
                pts2 = [(x, y), (x+size, y), (x+size//2, y+size)]
                if rng.random() < 0.7:
                    draw.polygon(pts1, fill=rand_color(rng.randint(60,180)))
                if rng.random() < 0.7:
                    draw.polygon(pts2, fill=rand_color(rng.randint(60,180)))

    elif composition == "soft_circles":
        # 겹치는 부드러운 원들
        for _ in range(rng.randint(8, 16)):
            x, y = rng.randint(-60, W+60), rng.randint(-60, H+60)
            r = rng.randint(30, 160)
            c = rand_color(rng.randint(40, 120))
            draw.ellipse([x-r, y-r, x+r, y+r], fill=c)

    elif composition == "waves":
        # 물결 레이어
        for i in range(rng.randint(6, 12)):
            y_base = i * (H // 10)
            pts = [(0, y_base)]
            for x in range(0, W+20, 20):
                wave = rng.randint(-30, 30)
                pts.append((x, y_base + wave))
            pts += [(W, H+10), (0, H+10)]
            c = rand_color(rng.randint(50, 150))
            draw.polygon(pts, fill=c)

    elif composition == "petals":
        # 꽃잎 형태 타원들
        cx, cy = W//2, H//2
        for i in range(rng.randint(6, 10)):
            angle = i * (360 / 8)
            dist  = rng.randint(60, 140)
            ex = cx + dist * math.cos(math.radians(angle))
            ey = cy + dist * math.sin(math.radians(angle))
            rw, rh = rng.randint(40, 90), rng.randint(20, 60)
            c = rand_color(rng.randint(60, 150))
            draw.ellipse([ex-rw, ey-rh, ex+rw, ey+rh], fill=c)

    elif composition == "crystal":
        # 수정 결정 구조
        for _ in range(rng.randint(8, 14)):
            x, y = rng.randint(30, W-30), rng.randint(30, H-30)
            h_size = rng.randint(30, 100)
            pts = [
                (x, y - h_size),
                (x + h_size//2, y - h_size//3),
                (x + h_size//3, y + h_size//2),
                (x - h_size//3, y + h_size//2),
                (x - h_size//2, y - h_size//3),
            ]
            c = rand_color(rng.randint(80, 180))
            draw.polygon(pts, fill=c)
            draw.polygon(pts, outline=(*palette[-1], 120), width=1)

    else:  # geometric_mix
        # 다양한 도형 혼합
        for _ in range(rng.randint(10, 18)):
            shape = rng.choice(["rect", "ellipse", "triangle", "line"])
            x, y = rng.randint(0, W), rng.randint(0, H)
            s = rng.randint(20, 150)
            c = rand_color(rng.randint(50, 170))
            if shape == "rect":
                draw.rectangle([x, y, x+s, y+rng.randint(20,s)], fill=c)
            elif shape == "ellipse":
                draw.ellipse([x-s//2, y-s//3, x+s//2, y+s//3], fill=c)
            elif shape == "triangle":
                pts = [(x, y), (x+s, y), (x+s//2, y-s)]
                draw.polygon(pts, fill=c)
            else:
                x2, y2 = rng.randint(0,W), rng.randint(0,H)
                draw.line([(x,y),(x2,y2)], fill=c, width=rng.randint(2,8))

    # ── 오버레이 합성 ──
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, overlay)
    img = img.convert('RGB')

    # ── 약한 블러로 부드럽게 ──
    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))

    # ── 하단 어두운 그라데이션 밴드 (책 표지 느낌) ──
    footer = Image.new('RGBA', (W, H), (0,0,0,0))
    fd = ImageDraw.Draw(footer)
    for i in range(100):
        alpha = int(180 * (i/100)**2)
        fd.line([(0, H-100+i),(W, H-100+i)], fill=(0,0,0,alpha))
    img = Image.alpha_composite(img.convert('RGBA'), footer)

    # ── 상단 얇은 밝은 선 (장식) ──
    accent_line = Image.new('RGBA', (W, H), (0,0,0,0))
    ald = ImageDraw.Draw(accent_line)
    ac = (*palette[-1], 120)
    ald.line([(0, 8),(W, 8)], fill=ac, width=3)
    img = Image.alpha_composite(img, accent_line)

    img = img.convert('RGB')
    img.save(filepath, "PNG", quality=95)
    print(f"[Cover Generator] 추상 표지 생성 완료: {filepath} (구도={composition})")
    return True


async def generate_book_cover_art(title: str, genre: str, synopsis: str, color: str = "#b54a6a", unique_id: str = None) -> Optional[str]:
    """
    책 내용 기반 추상 기하학 표지를 우선 생성하고, Imagen 3 / Pollinations.ai도 시도합니다.
    """
    try:
        os.makedirs("static/covers", exist_ok=True)
        if not unique_id:
            unique_id = secrets.token_hex(6)
        filename = f"cover_{unique_id}.png"
        filepath = os.path.join("static", "covers", filename)
        web_url = f"/static/covers/{filename}"

        # 이미 존재하는 경우 해당 경로 반환 (단, 5KB 미만은 단색 폴백으로 간주 → 재생성)
        if os.path.exists(filepath) and os.path.getsize(filepath) >= 5000:
            return web_url
        elif os.path.exists(filepath):
            os.remove(filepath)  # 단색 파일 삭제 후 재생성


        gemini_key = os.getenv("GEMINI_API_KEY")

        # ── 외부 AI API (Imagen 3) ──
        if gemini_key and gemini_key != "YOUR_GEMINI_API_KEY_HERE":
            mood = _analyze_book(genre, synopsis, title)
            palette = _pick_palette(mood, _hex_to_rgb(color))
            style_hint = (
                "mystical glowing abstract artwork" if mood["mystic"] else
                "cinematic dramatic artwork" if mood["dark"] else
                "soft romantic illustration" if mood["warm"] else
                "futuristic abstract concept art" if mood["scifi"] else
                "geometric abstract book cover art"
            )
            prompt_text = (
                f"{style_hint}, Korean literary novel, "
                f"inspired by: {(synopsis or '')[:80]}, "
                f"no text, no words, no letters, professional book jacket, "
                f"highly detailed, award-winning composition, 3:4 portrait"
            )
            imagen_url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:generateImages?key={gemini_key}"
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.post(imagen_url, headers={"Content-Type": "application/json"},
                                            json={"prompt": prompt_text, "numberOfImages": 1,
                                                  "aspectRatio": "3:4", "outputMimeType": "image/png"},
                                            timeout=8.0)
                    if res.status_code == 200:
                        data = res.json()
                        images = data.get("generatedImages", [])
                        if images and "image" in images[0]:
                            img_data = base64.b64decode(images[0]["image"]["imageBytes"])
                            with open(filepath, "wb") as f:
                                f.write(img_data)
                            print(f"[Cover Generator] Imagen 3 표지 생성 완료: {web_url}")
                            return web_url
            except Exception as e:
                print(f"[Cover Generator] Imagen 3 실패: {e}")

        # ── 2. Pollinations.ai — 실제 일러스트 이미지 생성 시도 ──
        try:
            mood = _analyze_book(genre, synopsis, title)
            genre_style_map = {
                "판타지": "epic fantasy illustration, mystical creatures, ethereal glow, magical atmosphere",
                "로맨스": "romantic illustration, soft warm light, delicate flowers, dreamy pastel aesthetic",
                "드라마": "cinematic dramatic illustration, emotional depth, chiaroscuro lighting",
                "드라마/로맨스": "romantic drama illustration, emotional warmth, soft cinematic lighting",
                "SF": "science fiction concept art, futuristic technology, neon accents, space motifs",
                "미스터리": "dark mystery illustration, moody noir atmosphere, shadow and silhouette",
                "스릴러": "thriller artwork, tense dark atmosphere, psychological tension",
                "역사": "historical illustration, period detail, ink and watercolor, aged texture",
                "공포": "horror artwork, eerie dark atmosphere, unsettling surreal elements",
            }
            style_hint = genre_style_map.get(genre, "literary fiction illustration, professional book jacket art")
            synopsis_snippet = (synopsis or "")[:100].strip()
            prompt_text = (
                f"{style_hint}, "
                f"inspired by: {synopsis_snippet}, "
                f"Korean novel book cover illustration, "
                f"no text, no letters, no words, no title, "
                f"professional artwork, highly detailed, "
                f"award-winning composition, 3:4 portrait format"
            )
            encoded_prompt = urllib.parse.quote(prompt_text)
            seed = random.randint(10000, 999999)
            poll_url = (
                f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                f"?width=450&height=600&nologo=true&seed={seed}&model=flux"
            )
            async with httpx.AsyncClient() as client:
                res = await client.get(poll_url, timeout=10.0)
                if res.status_code == 200 and len(res.content) > 5000:
                    with open(filepath, "wb") as f:
                        f.write(res.content)
                    print(f"[Cover Generator] Pollinations.ai 일러스트 표지 완료: {web_url}")
                    return web_url
        except Exception as poll_ex:
            print(f"[Cover Generator] Pollinations.ai 실패: {poll_ex}")

        # ── 3. 최후 수단: PIL 추상 기하학 표지 ──
        try:
            ok = _generate_abstract_cover_pil(title, genre, synopsis, color, filepath)
            if ok:
                return web_url
        except Exception as pil_ex:
            print(f"[Cover Generator] PIL 추상 표지 생성 실패: {pil_ex}")

    except Exception as ex:
        print(f"[Cover Generator] 표지 생성 중 예외 발생: {ex}")

    return None




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

# DB 스키마 동적 패치 (기존 DB 테이블에 새로운 컬럼이 없으면 추가)
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

        # candidate_books 테이블에 cover_image_url 컬럼 추가
        try:
            conn.execute(text("ALTER TABLE candidate_books ADD COLUMN cover_image_url VARCHAR(500);"))
            conn.commit()
            print("[DB Patch] Added 'cover_image_url' column to 'candidate_books' table.")
        except Exception:
            pass

        # books 테이블에 cover_image_url 컬럼 추가 (이미 있을 가능성 높음)
        try:
            conn.execute(text("ALTER TABLE books ADD COLUMN cover_image_url VARCHAR(500);"))
            conn.commit()
            print("[DB Patch] Added 'cover_image_url' column to 'books' table.")
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
        q1_text = f"독자님, 『{book.title}』 독서방에 오신 것을 환영합니다! 🎙️\n오늘 함께 나눌 추천 토론 질문입니다:\n\n1️⃣ 타인의 숨겨진 진짜 마음에 닿는 안경이 있다면, 쓰시겠습니까 아니면 모른 채 살아가시겠습니까?\n2️⃣ 여주인공 아델이 유리 렌즈를 닦을 때 느꼈던 서늘한 죄책감의 정체는 무엇일까요?\n3️⃣ 당신에게 잊고 싶지 않은 인생의 '가장 선명한 순간'은 언제인가요?\n\n자유롭게 의견을 남기시거나 @사회자에게 이야기를 건네보세요!"
        m1 = models.ChatMessage(book_id=book.id, user_id=moderator.id, content=q1_text, created_at=now_base)
        db.add(m1)
        db.commit()
        db.refresh(m1)
        
        # 2. 달빛독자
        m2 = models.ChatMessage(book_id=book.id, user_id=user_map["달빛독자"].id, content="저라면 그 안경 절대 안 쓸 것 같아요... 🙈 타인의 속마음을 전부 알게 되면 상처만 받을 것 같아서요. 아델이 3장에서 안경을 쓰자마자 후회했던 장면에서 온몸에 돋은 소름이 아직도 안 가시네요.", created_at=now_base + timedelta(minutes=5))
        db.add(m2)
        db.commit()
        db.refresh(m2)
        
        # 3. 새벽사서 (m2 답장)
        m3 = models.ChatMessage(book_id=book.id, user_id=user_map["새벽사서"].id, content="달빛독자님 의견에 완전 동의해요! 저도 보면서 마음이 덜컥 내려앉았어요. 아델이 상점 주인의 경고를 무시하고 렌즈를 쓸어 올렸을 때 그 서늘함이란... 차라리 모르는 게 약이라는 문장이 이번 책을 관통하는 핵심 같아요.", reply_to_id=m2.id, created_at=now_base + timedelta(minutes=10))
        db.add(m3)
        db.commit()
        db.refresh(m3)
        
        # 4. 밤의활자 (m3 답장)
        m4 = models.ChatMessage(book_id=book.id, user_id=user_map["밤의활자"].id, content="하지만 저는 조금 생각이 달라요! 억울한 오해를 풀거나 사랑하는 사람의 아픔을 읽을 수 있다면 불편함을 감수하고라도 쓸 것 같아요. 4장 정원 씬에서 주인공이 진실을 깨닫고 눈물 흘리는 장면이 저한텐 최고의 명장면이었거든요 😭", reply_to_id=m3.id, created_at=now_base + timedelta(minutes=15))
        db.add(m4)
        db.commit()
        db.refresh(m4)
        
        # 5. AI 사회자 (m4 답장)
        m5 = models.ChatMessage(book_id=book.id, user_id=moderator.id, content="밤의활자님, 진실을 감당하려는 그 용기 있는 관점이 참으로 눈부십니다. ✨ 타인의 아픔에 기꺼이 손을 뻗으려는 밤의활자님의 따스한 마음이 4장 정원의 햇살과 닮아있네요.\n\n글꽃소녀님과 구름산책님은 진실과 평온 중 어느 쪽에 더 마음이 기우시나요?", reply_to_id=m4.id, created_at=now_base + timedelta(minutes=20))
        db.add(m5)
        db.commit()
        db.refresh(m5)
        
        # 6. 글꽃소녀 (m5 답장)
        m6 = models.ChatMessage(book_id=book.id, user_id=user_map["글꽃소녀"].id, content="@사회자님! 저는 밤의활자님과 달빛독자님 중간인 것 같아요! 쓰긴 쓰되, 진짜 중요한 선택의 순간에만 아주 잠깐 쓸 것 같아요 ㅋㅋㅋ 아델이 안경을 닦을 때마다 나던 그 특유의 민트 향 묘사도 진짜 좋았어요.", reply_to_id=m5.id, created_at=now_base + timedelta(minutes=25))
        db.add(m6)
        db.commit()
        db.refresh(m6)
        
        db.add(m7)

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
        m1 = models.ChatMessage(book_id=book.id, user_id=user_map["바다의항해자"].id, content="지도 제작자 테오가 낡고 깨진 단안경을 닦을 때마다 렌즈 너머로 보이지 않는 운명의 해도가 그려지는 1장 도입부부터 몰입감이 진짜 대단하네요! 🌊", created_at=dt_july29_1)
        db.add(m1); db.commit(); db.refresh(m1)

        m2 = models.ChatMessage(book_id=book.id, user_id=user_map["단안경사색가"].id, content="맞아요! 렌즈에 금이 간 이유가 과거 거대한 폭풍우를 경고하다 깨진 것이란 비하인드를 읽고 소름 돋았습니다. 흩어진 해도의 조각들이 주인공 테오의 잊혀진 기억 자체였군요.", created_at=dt_july29_2)
        db.add(m2); db.commit(); db.refresh(m2)

        m3 = models.ChatMessage(book_id=book.id, user_id=user_map["해도의파수꾼"].id, content="단안경사색가님 관점에 완전 공감해요! 렌즈의 깨진 균열 선이 지도 상의 위험 해역 좌표와 딱 맞아떨어지는 연출이 참 고혹적이었어요 ⚓️", reply_to_id=m2.id, created_at=dt_july29_3)
        db.add(m3); db.commit(); db.refresh(m3)

        # Day 2: 7월 30일 (목)
        m4 = models.ChatMessage(book_id=book.id, user_id=user_map["문학유영가"].id, content="2장 안개 미궁 씬에서 동료들이 '이 이상 나아가면 파멸'이라고 외면할 때, 테오 혼자 단안경을 쥐고 선두에 서는 장면에서 눈물이 핑 돌았어요 😭 차라리 현실의 평온을 택할 순 없었을까요?", created_at=dt_july30_1)
        db.add(m4); db.commit(); db.refresh(m4)

        m5 = models.ChatMessage(book_id=book.id, user_id=user_map["꿈꾸는선장"].id, content="저는 테오의 선택을 지지해요! 진실을 외면한 평화는 언젠가 무너지는 모래성 같으니까요. 렌즈 너머로 비친 동료들의 진짜 갈망을 읽었기에 멈출 수 없었던 거죠.", reply_to_id=m4.id, created_at=dt_july30_2)
        db.add(m5); db.commit(); db.refresh(m5)

        m6 = models.ChatMessage(book_id=book.id, user_id=user_map["유리렌즈의비밀"].id, content="꿈꾸는선장님 말씀대로 2장의 시련은 단순한 항해가 아니라 스스로의 본 모습을 찾아가는 사색의 시련이었던 것 같아요 🌿", reply_to_id=m5.id, created_at=dt_july30_3)
        db.add(m6); db.commit(); db.refresh(m6)

        # Day 3: 7월 31일 (금)
        m7 = models.ChatMessage(book_id=book.id, user_id=user_map["항해사김민준"].id, content="'바다는 모든 것을 씻어내어 기억하지 않아도, 나의 해도는 끝내 너의 궤적을 기억한다' ... 3장 피날레 문장에 가슴이 먹먹해집니다. @사회자 님은 테오의 이 잃어버린 항해를 어떤 의미로 보시나요?", created_at=dt_july31_1)
        db.add(m7); db.commit(); db.refresh(m7)

        m8 = models.ChatMessage(book_id=book.id, user_id=moderator.id, content="항해사김민준님, 깊은 사색이 담긴 인상적인 문장을 짚어주셨네요. ✨ 테오에게 깨진 단안경은 과거의 상처를 들추는 아픔이 아니라, 잊혀진 사람들의 소망을 현실의 평화로 엮어내는 숭고한 창조의 계기였습니다.\n\n바다의항해자님과 단안경사색가님은 테오가 항해의 끝에서 되찾은 가장 소중한 궤적이 무엇이라고 생각하시나요?", reply_to_id=m7.id, created_at=dt_july31_2)
        db.add(m8); db.commit(); db.refresh(m8)

        m9 = models.ChatMessage(book_id=book.id, user_id=user_map["바다의항해자"].id, content="@사회자님! 테오가 되찾은 건 단순한 지도가 아니라 '함께 항해했던 동료들에 대한 깊은 신뢰'였다고 생각해요 😭 3장 마지막 햇살 씬이 그래서 너무 따뜻했습니다.", reply_to_id=m8.id, created_at=dt_july31_3)
        db.add(m9); db.commit(); db.refresh(m9)

        m10 = models.ChatMessage(book_id=book.id, user_id=user_map["단안경사색가"].id, content="맞아요! 상처 입은 렌즈로 보았기에 비로소 타인의 아픔을 가장 온전하게 품을 수 있었던 테오의 눈빛이 오래도록 잔상으로 남네요. 역대 최고의 활성화 독서방이었습니다 👏", reply_to_id=m9.id, created_at=dt_july31_4)
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
        
        # 문장 끝에 문장부호가 누락된 경우 안전하게 마침표 추가 (절대 이전 문장으로 자르지 않음)
        if final_content and not final_content[-1] in ['.', '?', '!', '"', "'", '⟩', '»', '✨', '🌿', '💬', '😭']:
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
    
    # AI 사회자 계정 및 『오래된 안경 상점과 갈망의 정원』 생동감 넘치는 시드 독서방 자동 생성
    db = database.SessionLocal()
    try:
        get_or_create_moderator(db)
        seed_glass_shop_book_if_needed(db)
        seed_lost_voyage_book_if_needed(db)
        print("AI Moderator & Book Seeds (Glass Shop & Lost Voyage) initialized successfully.")
    except Exception as e:
        print(f"Error initializing AI Moderator or Seed data: {e}")
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
async def generate_candidates(background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    """
    Google Gemini API를 호출하여 세상에 없는 독창적인 책을 실시간 생성하거나 Pool에서 가져와 3개의 후보를 반환합니다.
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
    
    # 0. 이전에 선택하지 않고 'pending'으로 남아있는 후보들을 먼저 'pool'로 정리
    db.query(models.CandidateBook).filter(models.CandidateBook.status == 'pending').update({"status": "pool"})
    db.flush()

    # 1. Pool(보관된 남겨진 책들) 중에서 매번 무작위 랜덤으로 꺼내오기 (최대 3권)
    reused_candidates = db.query(models.CandidateBook).filter(
        models.CandidateBook.status == 'pool'
    ).order_by(
        func.random()
    ).limit(3).all()
    
    needed_count = 3 - len(reused_candidates)
    
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
                    generate_book_cover_art(c.title, c.genre, c.synopsis, c.color, f"cand_{c.id}")
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
        candidate.cover_image_url = await generate_book_cover_art(candidate.title, candidate.genre, candidate.synopsis, candidate.color, f"cand_{candidate.id}")
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
    
    moderator = get_or_create_moderator(db)
    has_mod_msg = any(m.user_id == moderator.id for m in messages)
    
    # 해당 독서방에 AI 사회자 질문 메시지가 없는 경우 (기존 방 포함) 첫 웰컴 카드 자동 생성
    if not has_mod_msg:
        try:
            target_bid = int(book_id)
        except (ValueError, TypeError):
            target_bid = book_id
            
        book = db.query(models.Book).filter(models.Book.id == target_bid).first()
        if book and moderator:
            q_list = []
            if book.core_dilemma:
                q_list.append(f"1️⃣ {book.core_dilemma.replace('Q. ', '')}")
            if book.additional_questions:
                add_qs = [q.strip().replace('Q. ', '') for q in book.additional_questions.split('|') if q.strip()]
                for idx, q in enumerate(add_qs[:2], start=len(q_list)+1):
                    q_list.append(f"{idx}️⃣ {q}")
            
            if not q_list:
                q_list = ["1️⃣ 이 책의 주인공의 선택에 대해 어떻게 생각하시나요?"]
                
            q_text = "\n".join(q_list)
            welcome_text = f"독자님, 『{book.title}』 독서방에 오신 것을 환영합니다! 🎙️\n오늘 함께 나눌 추천 토론 질문입니다:\n\n{q_text}\n\n자유롭게 의견을 남기시거나 @사회자에게 이야기를 건네보세요!"
            
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
