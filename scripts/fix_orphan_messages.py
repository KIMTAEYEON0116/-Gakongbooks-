# -*- coding: utf-8 -*-
"""주인 없는 채팅 메시지를 정리한다.

예전 DB에서 옮겨 온 시드(샘플) 대화는 user_id가 옛 번호라 지금 users 표에 없다.
그 글은 화면에서 전부 '독자/読者'로 보이고, 아카이브의 참여자 목록에서도 이름이 사라진다.
이름은 백업에도 남아 있지 않아 되살릴 수 없다. 대신 서비스 소개용 샘플 독자 계정
(@gakong.com, 화면에 '예시' 표시)에 옛 번호별로 하나씩 고정 배정해, 같은 사람의
글은 같은 이름으로 이어지게 한다. 사회자 환영문 복제본(사회자 글과 같은 환영문인데
주인이 없는 것)은 지운다.

실행:  cd ~/-Gakongbooks- && PYTHONPATH=. venv/bin/python scripts/fix_orphan_messages.py          # 미리 보기
       cd ~/-Gakongbooks- && PYTHONPATH=. venv/bin/python scripts/fix_orphan_messages.py --apply  # 적용
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(errors="replace")

import database  # noqa: E402
import main      # noqa: E402
import models    # noqa: E402

APPLY = "--apply" in sys.argv
db = database.SessionLocal()

users = {u.id: u for u in db.query(models.User).all()}
samples = sorted([u for u in users.values() if main.is_sample_user(u)], key=lambda u: u.id)
if not samples:
    print("샘플 독자 계정이 없어 배정할 수 없다."); sys.exit(1)

msgs = db.query(models.ChatMessage).order_by(models.ChatMessage.id).all()
orphans = [m for m in msgs if m.user_id not in users]
print(f"주인 없는 메시지 {len(orphans)}건 / 샘플 계정 {len(samples)}개")

# 1) 사회자 환영문 복제본은 지운다
deleted = []
for m in orphans:
    if main.WELCOME_MARKER in (m.content or ""):
        deleted.append(m)
print(f"지울 환영문 복제본: {[m.id for m in deleted] or '없음'}")

# 2) 나머지는 옛 user_id별로 샘플 계정을 고정 배정한다 (책마다 번호가 겹치지 않게 순환)
remaining = [m for m in orphans if m not in deleted]
old_ids = sorted({m.user_id for m in remaining})
assign = {old: samples[i % len(samples)] for i, old in enumerate(old_ids)}
print("배정 표 (옛 번호 → 샘플 닉네임):")
for old, u in assign.items():
    n = sum(1 for m in remaining if m.user_id == old)
    print(f"  {old:>4} → {u.nickname} ({n}건)")

if not APPLY:
    print("\n미리 보기만 했다. 적용하려면 --apply 를 붙인다.")
    db.close(); sys.exit(0)

for m in deleted:
    db.query(models.ChatMessage).filter(models.ChatMessage.reply_to_id == m.id).update({"reply_to_id": None})
    db.delete(m)
for m in remaining:
    m.user_id = assign[m.user_id].id
db.commit()
print(f"\n적용 완료: 삭제 {len(deleted)}건, 재배정 {len(remaining)}건")
db.close()
