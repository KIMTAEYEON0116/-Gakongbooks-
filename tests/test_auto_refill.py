# -*- coding: utf-8 -*-
# 실행: 저장소 루트에서  python tests/test_auto_refill.py
"""활성 독서방 자동 보충을 확인한다. 외부 API는 부르지 않는다(대비 템플릿으로 만든다).

  1. 열린 방이 1권이면 3권까지 채운다
  2. 이미 3권이면 아무것도 만들지 않는다
  3. 보충이 돌아도 다른 사용자가 고르는 중인 후보는 그대로 남는다
"""
import asyncio
import os
import sys

sys.path.insert(0, os.getcwd())
sys.stdout.reconfigure(errors="replace")

from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

import database  # noqa: E402
import main      # noqa: E402
import models    # noqa: E402

eng = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
models.Base.metadata.create_all(eng)
Session = sessionmaker(bind=eng)
database.SessionLocal = Session
main.database.SessionLocal = Session


async def _dead(*a, **k):
    return None


async def _fake_cover(*a, **k):
    return "/static/covers/test.png"


async def _fake_translate(*a, **k):
    return True


main.gemini_request = _dead
main.generate_book_cover_art = _fake_cover
main.translate_book_to_ja = _fake_translate
main.translate_candidates_to_ja = _dead

results = []


def check(label, ok, extra=""):
    results.append(ok)
    print(("  [통과] " if ok else "  [실패] ") + label + (" " + extra if extra else ""))


db = Session()
common = dict(author="a", genre="SF", synopsis="s", tags="#t", price="₩1", page_count=1, deadline_days=10)
db.add(models.Book(title="유일한 열린 방", is_archived=False, **common))
db.add(models.Book(title="종료된 방", is_archived=True, **common))
user = models.User(email="u@example.com", password_hash="x", nickname="고르는중")
db.add(user)
db.commit()
db.add(models.CandidateBook(title="남의 후보", author="a", genre="SF", synopsis="s", tags="#t",
                            status="pending", created_by=user.id))
db.commit()
db.close()

asyncio.run(main._auto_refill_active_books_if_needed())

db = Session()
active = db.query(models.Book).filter(models.Book.is_archived.is_(False)).count()
check("열린 방 1권 → 3권으로 보충", active == main.MIN_ACTIVE_BOOKS, f"(현재 {active}권)")
other = db.query(models.CandidateBook).filter(models.CandidateBook.title == "남의 후보").first()
check("다른 사용자가 고르는 중인 후보는 그대로 pending", other is not None and other.status == "pending",
      f"(상태 {other.status if other else None})")
adopted = db.query(models.CandidateBook).filter(models.CandidateBook.status == "adopted").count()
check("보충에 쓴 후보는 adopted 로 기록된다", adopted == main.MIN_ACTIVE_BOOKS - 1, f"({adopted}건)")
db.close()

asyncio.run(main._auto_refill_active_books_if_needed())
db = Session()
active2 = db.query(models.Book).filter(models.Book.is_archived.is_(False)).count()
check("이미 3권이면 더 만들지 않는다", active2 == active, f"(현재 {active2}권)")
db.close()

print()
print("결과: " + ("모두 통과" if all(results) else "%d건 실패" % results.count(False)))
sys.exit(0 if all(results) else 1)
