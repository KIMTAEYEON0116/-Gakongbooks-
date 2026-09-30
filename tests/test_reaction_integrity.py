# -*- coding: utf-8 -*-
# 실행: 저장소 루트에서  python tests/test_reaction_integrity.py
"""반응 조작 테스트 — 실제 API 경로(/api/chats/{id}/react)로 요청한다.

예전에는 반응이 숫자로만 저장되어 누가 눌렀는지 몰랐다. 그래서
  - 한 사람이 같은 요청을 반복해 하트를 무한히 올릴 수 있었고
  - 취소를 반복하면 남이 누른 반응까지 0으로 깎을 수 있었다.

메모리 SQLite에서 돌아 실제 데이터는 건드리지 않는다.
"""
import os
import sys

sys.path.insert(0, os.getcwd())
sys.stdout.reconfigure(errors="replace")

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import auth      # noqa: E402
import database  # noqa: E402
import main      # noqa: E402
import models    # noqa: E402

HEART = "❤️"

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

db = Session()
a = models.User(email="a@t.com", nickname="글쓴이", password_hash="x")
b = models.User(email="b@t.com", nickname="독자B", password_hash="x")
c = models.User(email="c@t.com", nickname="독자C", password_hash="x")
book = models.Book(title="t", author="a", genre="g", synopsis="s", tags="", price="0",
                   page_count=1, color="#000", deadline_days=10, is_archived=False)
db.add_all([a, b, c, book]); db.flush()
# 표본 대화에 남아 있는 예전 반응(누가 눌렀는지 모르는 숫자)을 기준선으로 둔다
msg = models.ChatMessage(book_id=book.id, user_id=a.id, content="글", reactions='{"%s": 5}' % HEART)
db.add(msg); db.commit()
A, B, C, MID = a.id, b.id, c.id, msg.id

client = TestClient(main.app)
ok = True


def hearts(resp):
    return resp.json().get("reactions", {}).get(HEART, 0)


def expect(label, cond, detail=""):
    global ok
    ok &= bool(cond)
    print("  [%s] %s %s" % ("통과" if cond else "실패", label, detail))


# 1) 한 사람이 같은 반응을 반복해도 1번만 반영된다
who["id"] = B
first = client.post("/api/chats/%d/react" % MID, json={"emoji": HEART})
for _ in range(20):
    last = client.post("/api/chats/%d/react" % MID, json={"emoji": HEART})
expect("같은 반응 21번 요청 → 1만 증가", hearts(last) == 6, "(기준선 5 → %d)" % hearts(last))
expect("내가 누른 반응으로 표시됨", HEART in last.json().get("mine", []))

# 2) 다른 사람이 누르면 따로 쌓인다
who["id"] = C
r = client.post("/api/chats/%d/react" % MID, json={"emoji": HEART})
expect("다른 사람이 누르면 +1", hearts(r) == 7, "(%d)" % hearts(r))

# 3) 취소는 내 기록만 지운다
who["id"] = C
for _ in range(10):
    r = client.delete("/api/chats/%d/react?emoji=%s" % (MID, HEART))
expect("취소 10번 반복해도 내 것 1개만 사라짐", hearts(r) == 6, "(%d)" % hearts(r))
expect("남이 누른 반응은 그대로", hearts(r) >= 6)

s = Session(); left = s.query(models.ChatReaction).filter_by(message_id=MID).count(); s.close()
expect("기록 테이블에는 B의 1건만 남음", left == 1, "(%d건)" % left)

# 4) 기준선은 깎이지 않는다
who["id"] = B
for _ in range(10):
    r = client.delete("/api/chats/%d/react?emoji=%s" % (MID, HEART))
expect("모두 취소해도 예전 반응 5는 유지", hearts(r) == 5, "(%d)" % hearts(r))

# 5) 자기 글에는 반응할 수 없다
who["id"] = A
r = client.post("/api/chats/%d/react" % MID, json={"emoji": HEART})
expect("자기 글에 반응 → 거부", r.status_code == 400, "(응답 %d)" % r.status_code)

# 6) 목록 조회에도 내가 누른 표시가 실린다
who["id"] = C
client.post("/api/chats/%d/react" % MID, json={"emoji": HEART})
lst = client.get("/api/books/%d/chats" % book.id).json()
row = [m for m in lst if m["id"] == MID][0]
expect("목록 응답에 myReactions 포함", HEART in row.get("myReactions", []), "(%s)" % row.get("myReactions"))

print("결과:", "전부 통과" if ok else "실패 있음")
sys.exit(0 if ok else 1)
