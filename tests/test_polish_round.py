# -*- coding: utf-8 -*-
# 실행: 저장소 루트에서  python tests/test_polish_round.py
"""운영 점검에서 고친 네 가지를 확인한다.

  1. /health 가 서버·DB 상태를 돌려준다
  2. 체험 계정은 '하루 1회'가 아니라 쿨다운으로 생성 제한을 받는다
  3. 환영 카드는 책 번역이 있으면 AI 없이 일본어본이 함께 저장된다
  4. 비밀번호 재설정 메일은 일본어·한국어를 함께 담는다

메모리 SQLite에서 돌아 실제 데이터는 건드리지 않는다. Gemini는 부르지 않는다.
"""
import asyncio
import os
import sys
from datetime import timedelta

sys.path.insert(0, os.getcwd())
sys.stdout.reconfigure(errors="replace")

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

import auth      # noqa: E402
import config    # noqa: E402
import database  # noqa: E402
import main      # noqa: E402
import models    # noqa: E402

eng = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
models.Base.metadata.create_all(eng)
Session = sessionmaker(bind=eng)


def get_test_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


main.app.dependency_overrides[database.get_db] = get_test_db
who = {"id": None}
main.app.dependency_overrides[auth.get_current_user_id] = lambda: who["id"]
main.app.dependency_overrides[auth.get_current_user_id_optional] = lambda: who["id"]


async def _dead(*a, **k):
    return None


main.gemini_request = _dead                      # AI는 전혀 응답하지 않는 날이라고 가정
main.translate_moderator_message_to_ja = _dead   # 백그라운드 번역도 막는다

client = TestClient(main.app)
results = []


def check(label, ok, extra=""):
    results.append(ok)
    print(("  [통과] " if ok else "  [실패] ") + label + (" " + extra if extra else ""))


# ── 1. /health ──
r = client.get("/health")
check("/health 가 200과 status=ok 를 돌려준다", r.status_code == 200 and r.json().get("status") == "ok", str(r.json()))

# ── 준비: 체험 계정 · 일반 계정 · 책 ──
db = Session()
demo = models.User(email=config.DEMO_EMAIL, password_hash="x", nickname="体験")
normal = models.User(email="n@example.com", password_hash="x", nickname="보통독자")
db.add_all([demo, normal])
db.commit()
demo_id, normal_id = demo.id, normal.id
db.close()


def produce_fake(db, background_tasks, owner_user_id=None, count=3):
    return []


async def _produce(*a, **k):
    return []


main._produce_candidate_books = _produce

# ── 2. 체험 계정 쿨다운 ──
db = Session()
u = db.get(models.User, demo_id)
u.last_generation_at = models.get_kst_now() - timedelta(minutes=config.DEMO_GENERATION_COOLDOWN_MINUTES + 5)
db.commit()
db.close()
who["id"] = demo_id
r1 = client.post("/api/books/candidates", headers={"X-App-Lang": "ja"})
r2 = client.post("/api/books/candidates", headers={"X-App-Lang": "ja"})
check("체험 계정: 같은 날이라도 쿨다운이 지났으면 생성할 수 있다", r1.status_code == 200, str(r1.status_code))
check("체험 계정: 바로 이어서는 429 + 일본어 안내", r2.status_code == 429 and "体験アカウント" in r2.json().get("detail", ""),
      r2.json().get("detail", "")[:40] if r2.status_code == 429 else str(r2.status_code))

db = Session()
u = db.get(models.User, normal_id)
u.last_generation_at = models.get_kst_now() - timedelta(minutes=config.DEMO_GENERATION_COOLDOWN_MINUTES + 5)
db.commit()
db.close()
who["id"] = normal_id
r3 = client.post("/api/books/candidates", headers={"X-App-Lang": "ja"})
check("일반 계정: 하루 1회 규칙은 그대로다 (오늘 이미 만들었으면 429)", r3.status_code == 429, str(r3.status_code))

# ── 3. 환영 카드 일본어본 ──
db = Session()
book_ja = models.Book(
    title="해피엔딩을 묻는 오르골의 시간", author="니시노 켄지", genre="추리/미스터리",
    synopsis="줄거리", tags="#미스터리", price="₩18,000", page_count=340,
    core_dilemma="Q. 행복한 결말은 누구를 위한 것일까요?",
    additional_questions="오르골의 침묵은 무엇을 뜻할까요?|주인공의 선택을 어떻게 보시나요?",
    i18n_ja='{"title":"ハッピーエンドを問うオルゴールの時間","core_dilemma":"Q. 幸せな結末は誰のためのものでしょうか。",'
            '"additional_questions":"オルゴールの沈黙は何を意味するのでしょうか。|主人公の選択をどうご覧になりますか。"}',
    deadline_days=10,
)
book_ko = models.Book(
    title="번역 없는 책", author="저자", genre="SF", synopsis="줄거리", tags="#SF",
    price="₩15,000", page_count=200, core_dilemma="Q. 질문?", deadline_days=10,
)
db.add_all([book_ja, book_ko])
db.commit()
bid_ja, bid_ko = book_ja.id, book_ko.id
db.close()

who["id"] = None
hist = client.get(f"/api/books/{bid_ja}/chats").json()
welcome = [h for h in hist if h["isBot"] and main.WELCOME_MARKER in h["text"]]
ja_body = (welcome[0].get("textJa") or "") if welcome else ""
check("번역된 책: 환영 카드에 일본어본이 바로 붙는다 (AI 호출 없이)",
      bool(welcome) and "ハッピーエンド" in ja_body and "@司会者" in ja_body and "주인공" not in ja_body,
      ja_body[:40])
check("번역된 책: 일본어본에 질문 세 개가 번호로 들어간다",
      "1. 幸せな結末" in ja_body and "2. オルゴール" in ja_body and "3. 主人公" in ja_body)

hist2 = client.get(f"/api/books/{bid_ko}/chats").json()
welcome2 = [h for h in hist2 if h["isBot"] and main.WELCOME_MARKER in h["text"]]
check("번역 없는 책: 반쪽짜리 일본어본을 만들지 않는다 (AI 번역에 맡긴다)",
      bool(welcome2) and not welcome2[0].get("textJa"))

# ── 4. 재설정 메일 병기 ──
sent = {}


def fake_send(to_email, subject, body):
    sent["subject"], sent["body"] = subject, body
    return True


main._send_email = fake_send
main.send_reset_link_email("x@example.com", "読者", "http://example.com/reset-password?token=abc")
check("재설정 메일 제목에 일본어가 있다", "パスワード再設定" in sent.get("subject", ""))
check("재설정 메일 본문에 일본어·한국어가 함께 있고 링크가 들어 있다",
      "再設定" in sent.get("body", "") and "재설정" in sent.get("body", "") and "token=abc" in sent.get("body", ""))

print()
print("결과: " + ("모두 통과" if all(results) else "%d건 실패" % results.count(False)))
sys.exit(0 if all(results) else 1)
