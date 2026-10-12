# -*- coding: utf-8 -*-
# 실행: 저장소 루트에서  python tests/test_user_translation.py
"""독자 글 묶음 번역을 확인한다. 외부 API는 가짜 응답으로 대신한다.

  1. 한글 글에는 일본어본이, 일본어 글에는 한국어본이 붙는다 (한 번의 호출로)
  2. 사회자 글과 이미 번역된 글은 대상에서 빠진다
  3. 결과에 상대 언어 문자가 섞이면 그 글만 버린다
  4. 대화 API가 textKo 를 함께 내려준다
"""
import asyncio
import os
import sys

sys.path.insert(0, os.getcwd())
sys.stdout.reconfigure(errors="replace")

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

import auth      # noqa: E402
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
main.app.dependency_overrides[auth.get_current_user_id_optional] = lambda: None
results = []


def check(label, ok, extra=""):
    results.append(ok)
    print(("  [통과] " if ok else "  [실패] ") + label + (" " + extra if extra else ""))


db = Session()
book = models.Book(title="책", author="a", genre="SF", synopsis="s", tags="#t", price="₩1", page_count=1, deadline_days=10)
bot = models.User(email=main.MODERATOR_EMAIL, password_hash="x", nickname=main.MODERATOR_NICKNAME, is_bot=True)
ko_user = models.User(email="ko@example.com", password_hash="x", nickname="한국독자")
ja_user = models.User(email="ja@example.com", password_hash="x", nickname="日本読者")
db.add_all([book, bot, ko_user, ja_user]); db.commit()
m_ko = models.ChatMessage(book_id=book.id, user_id=ko_user.id, content="이 책 정말 좋았어요.")
m_ja = models.ChatMessage(book_id=book.id, user_id=ja_user.id, content="この本、とても良かったです。")
m_bot = models.ChatMessage(book_id=book.id, user_id=bot.id, content="사회자 글입니다.")
m_done = models.ChatMessage(book_id=book.id, user_id=ko_user.id, content="이미 번역됨", content_ja="翻訳済み")
m_bad = models.ChatMessage(book_id=book.id, user_id=ko_user.id, content="섞인 응답을 받을 글")
db.add_all([m_ko, m_ja, m_bot, m_done, m_bad]); db.commit()
ids = {"ko": m_ko.id, "ja": m_ja.id, "bot": m_bot.id, "done": m_done.id, "bad": m_bad.id}
bid = book.id
db.close()

calls = {"n": 0, "keys": None}


async def fake_gemini_json(prompt, timeout=40.0):
    calls["n"] += 1
    import json
    import re
    src = json.loads(re.search(r"\[원문 JSON\]\s*(\{.*?\n\s*\})\s*\n\s*\[원칙\]", prompt, re.S).group(1))
    calls["keys"] = sorted(src.keys())
    out = {}
    for k, v in src.items():
        if int(k) == ids["ko"]:
            out[k] = "この本、本当に良かったです。"
        elif int(k) == ids["ja"]:
            out[k] = "이 책, 정말 좋았어요."
        elif int(k) == ids["bad"]:
            out[k] = "일부 한글이 남은 翻訳"
    return out


main._gemini_json = fake_gemini_json

db = Session()
n = asyncio.run(main.translate_user_messages_batch(db))
db.close()

db = Session()
check("한 번의 호출로 묶어 번역한다", calls["n"] == 1, f"(호출 {calls['n']}회)")
check("대상은 한글 글·일본어 글·섞일 글 셋뿐 (사회자·번역된 글 제외)",
      calls["keys"] == sorted(str(ids[k]) for k in ("ko", "ja", "bad")), str(calls["keys"]))
check("한글 글 → 일본어본 저장", db.get(models.ChatMessage, ids["ko"]).content_ja == "この本、本当に良かったです。")
check("일본어 글 → 한국어본 저장", db.get(models.ChatMessage, ids["ja"]).content_ko == "이 책, 정말 좋았어요.")
check("한글이 섞인 일본어 결과는 버린다", not db.get(models.ChatMessage, ids["bad"]).content_ja)
check("저장 건수는 2", n == 2, f"({n})")
db.close()

client = TestClient(main.app)
hist = client.get(f"/api/books/{bid}/chats", headers={"X-App-Lang": "ko"}).json()
ja_msg = next(h for h in hist if h["id"] == ids["ja"])
check("대화 API가 일본어 글의 한국어본(textKo)을 내려준다", ja_msg.get("textKo") == "이 책, 정말 좋았어요.")

print()
print("결과: " + ("모두 통과" if all(results) else "%d건 실패" % results.count(False)))
sys.exit(0 if all(results) else 1)
