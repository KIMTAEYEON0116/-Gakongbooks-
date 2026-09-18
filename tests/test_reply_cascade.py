# -*- coding: utf-8 -*-
# 실행: 저장소 루트에서  python tests/test_reply_cascade.py
"""답글 연쇄 삭제 재현 테스트.

A가 글을 쓰고 B가 거기에 답글을 단다. 그다음
  (1) A가 자기 글을 지우는 경우
  (2) A가 탈퇴하는 경우
두 경우 모두 B의 답글은 남아 있어야 한다. 인용 대상만 사라지고(reply_to_id=NULL).

실제 DB는 건드리지 않는다. 메모리 SQLite에 테이블을 새로 만들어 쓴다.
"""
import os
import sys

sys.path.insert(0, os.getcwd())
sys.stdout.reconfigure(errors="replace")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models  # noqa: E402


def fresh():
    eng = create_engine("sqlite://")
    models.Base.metadata.create_all(eng)
    db = sessionmaker(bind=eng)()
    a = models.User(email="a@test.com", nickname="A", password_hash="x")
    b = models.User(email="b@test.com", nickname="B", password_hash="x")
    book = models.Book(title="t", author="a", genre="g", synopsis="s", tags="", price="0",
                       page_count=1, color="#000", deadline_days=10, is_archived=False)
    db.add_all([a, b, book]); db.flush()
    parent = models.ChatMessage(book_id=book.id, user_id=a.id, content="A의 글")
    db.add(parent); db.flush()
    reply = models.ChatMessage(book_id=book.id, user_id=b.id, content="B의 답글", reply_to_id=parent.id)
    db.add(reply); db.commit()
    return db, a, parent, reply.id


def check(label, db, reply_id):
    db.expire_all()
    r = db.get(models.ChatMessage, reply_id)
    if r is None:
        print("  [실패] %s → B의 답글이 함께 삭제됨" % label); return False
    print("  [통과] %s → B의 답글 유지, 인용 대상=%s" % (label, r.reply_to_id)); return True


ok = True
db, a, parent, rid = fresh()
db.delete(parent); db.commit()
ok &= check("A가 자기 글 삭제", db, rid)

db, a, parent, rid = fresh()
db.delete(a); db.commit()
ok &= check("A가 탈퇴", db, rid)

print("결과:", "전부 통과" if ok else "실패 있음")
sys.exit(0 if ok else 1)
