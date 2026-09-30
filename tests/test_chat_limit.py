# -*- coding: utf-8 -*-
# 실행: 저장소 루트에서  python tests/test_chat_limit.py
"""채팅 도배 차단 테스트 — 실제 API 경로(/api/books/{id}/chats)로 요청한다.

예전에는 메시지 전송에 횟수 제한이 없어 계정 하나로 방을 가득 채울 수 있었고,
공백만 보낸 빈 메시지도 그대로 저장됐다.

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


def make_book(title):
    b = models.Book(title=title, author="a", genre="g", synopsis="s", tags="", price="0",
                    page_count=1, color="#000", deadline_days=10, is_archived=False)
    db.add(b); db.flush()
    return b.id


db = Session()
u1 = models.User(email="u1@t.com", nickname="독자1", password_hash="x")
u2 = models.User(email="u2@t.com", nickname="독자2", password_hash="x")
db.add_all([u1, u2]); db.flush()
B1, B2, B3 = make_book("방1"), make_book("방2"), make_book("방3")
db.commit()
U1, U2 = u1.id, u2.id

client = TestClient(main.app)
ok = True


def expect(label, cond, detail=""):
    global ok
    ok &= bool(cond)
    print("  [%s] %s %s" % ("통과" if cond else "실패", label, detail))


def send(book_id, text):
    return client.post("/api/books/%d/chats" % book_id, json={"text": text})


# 1) 공백만 있는 메시지는 저장되지 않는다
who["id"] = U1
r = send(B1, "   ")
expect("공백만 보낸 메시지 → 거부", r.status_code == 400, "(응답 %d)" % r.status_code)

# 2) 한 방에 1분 10건까지만 보낼 수 있다
who["id"] = U1
codes = [send(B2, "감상 %d" % i).status_code for i in range(12)]
expect("앞의 10건은 전송 성공", codes[:10].count(200) == 10, "(%s)" % codes[:10])
expect("11번째부터 차단(429)", codes[10] == 429 and codes[11] == 429, "(%s)" % codes[10:])

s = Session(); saved = s.query(models.ChatMessage).filter_by(book_id=B2).count(); s.close()
expect("실제로 저장된 것도 10건", saved == 10, "(%d건)" % saved)

# 3) 제한은 사람과 방 단위다 — 남의 전송까지 막으면 안 된다
who["id"] = U2
expect("다른 사람은 같은 방에 보낼 수 있음", send(B2, "다른 독자의 감상").status_code == 200)
who["id"] = U1
expect("같은 사람도 다른 방에는 보낼 수 있음", send(B3, "다른 방의 감상").status_code == 200)

print("결과:", "전부 통과" if ok else "실패 있음")
sys.exit(0 if ok else 1)
