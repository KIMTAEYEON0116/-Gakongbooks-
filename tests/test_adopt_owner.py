# -*- coding: utf-8 -*-
# 실행: 저장소 루트에서  python tests/test_adopt_owner.py
"""후보 채택 소유권 테스트 — 실제 API 경로(/api/books/adopt/{id})로 요청한다.

메모리 SQLite를 get_db에 끼워 넣고, 로그인 사용자도 바꿔 끼운다.
lifespan(백그라운드 루프·시드)은 돌지 않도록 TestClient를 with 없이 쓴다.
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

db = Session()
a = models.User(email="a@test.com", nickname="A", password_hash="x")
b = models.User(email="b@test.com", nickname="B", password_hash="x")
db.add_all([a, b]); db.flush()


def cand(owner, title):
    c = models.CandidateBook(title=title, author="작가", genre="소설", synopsis="줄거리", tags="#태그",
                             status="pending", created_by=owner, cover_image_url="/static/covers/x.png")
    db.add(c); db.flush()
    return c.id


a1, a2 = cand(a.id, "A의 후보1"), cand(a.id, "A의 후보2")
b1 = cand(b.id, "B의 후보1")
sys_c = cand(None, "주인 없는 후보")
db.commit()
A, B = a.id, b.id

client = TestClient(main.app)
ok = True


def status_of(cid):
    s = Session(); v = s.get(models.CandidateBook, cid).status; s.close(); return v


def expect(label, cond, detail=""):
    global ok
    ok &= bool(cond)
    print("  [%s] %s %s" % ("통과" if cond else "실패", label, detail))


# 1) B가 A의 후보를 가로채려 함
who["id"] = B
r = client.post("/api/books/adopt/%d" % a1)
expect("B가 A의 후보 채택 시도 → 거부", r.status_code == 404, "(응답 %d)" % r.status_code)
expect("A의 후보 두 권은 그대로 pending", status_of(a1) == "pending" and status_of(a2) == "pending",
       "(%s, %s)" % (status_of(a1), status_of(a2)))

# 2) 주인 없는 후보도 채택 불가
r = client.post("/api/books/adopt/%d" % sys_c)
expect("주인 없는 후보 채택 시도 → 거부", r.status_code == 404, "(응답 %d)" % r.status_code)
expect("그때 다른 사람 후보가 pool로 쓸려가지 않음", status_of(a1) == "pending" and status_of(b1) == "pending")

# 3) A 본인은 정상 채택
who["id"] = A
r = client.post("/api/books/adopt/%d" % a1)
expect("A가 자기 후보 채택 → 성공", r.status_code == 200, "(응답 %d)" % r.status_code)
expect("채택한 후보는 adopted, 남은 A 후보는 pool", status_of(a1) == "adopted" and status_of(a2) == "pool",
       "(%s, %s)" % (status_of(a1), status_of(a2)))
expect("B의 후보는 영향 없음", status_of(b1) == "pending", "(%s)" % status_of(b1))
s = Session(); n = s.query(models.Book).count(); s.close()
expect("도서가 정확히 1권 생성", n == 1, "(%d권)" % n)

print("결과:", "전부 통과" if ok else "실패 있음")
sys.exit(0 if ok else 1)
