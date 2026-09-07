# -*- coding: utf-8 -*-
"""일본어 번역본을 파일로 내보내고 다시 넣는다.

번역문은 지금 MySQL 안에만 있다. DB를 새로 만들거나 옮기면 통째로 사라지고,
Gemini 무료 한도(하루 20건)로는 다시 만들 수도 없다. 그래서 파일로 남긴다.

  python scripts/ja_translations.py dump      DB → data/ja_translations.json
  python scripts/ja_translations.py restore   data/ja_translations.json → DB

메시지는 아이디가 아니라 '책 + 작성자 + 원문'으로 찾는다.
아이디는 아카이브 이관 때 바뀌지만 원문은 그대로이기 때문이다.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database  # noqa: E402
import models    # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "data", "ja_translations.json")

# 도서 i18n_ja 안에서 내보낼 항목
BOOK_FIELDS = ["title", "author", "genre", "synopsis", "tags", "toc",
               "memorable_quote", "endorsement_quote", "endorsement_attr",
               "closing_remark", "characters"]


def msg_key(m):
    """이관으로 아이디가 바뀌어도 같은 메시지를 가리키는 열쇠."""
    return "%d|%d|%s" % (m.book_id, m.user_id, (m.content or "").strip())


def dump():
    db = database.SessionLocal()
    books = {}
    for b in db.query(models.Book).all():
        d = json.loads(b.i18n_ja or "{}")
        if not d:
            continue
        books[b.title] = {k: v for k, v in d.items() if k in BOOK_FIELDS and v}

    messages = {}
    for Model in (models.ChatMessage, models.PastChatMessage):
        for m in db.query(Model).all():
            if m.content_ja:
                messages[msg_key(m)] = m.content_ja
    db.close()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"books": books, "messages": messages}, f,
                  ensure_ascii=False, indent=2, sort_keys=True)
    print("내보냄: 도서 %d권 · 메시지 %d건 → %s" % (len(books), len(messages), OUT))


def restore():
    with io.open(OUT, encoding="utf-8") as f:
        data = json.load(f)

    db = database.SessionLocal()
    nb = nm = 0

    for b in db.query(models.Book).all():
        saved = data["books"].get(b.title)
        if not saved:
            continue
        cur = json.loads(b.i18n_ja or "{}")
        cur.update(saved)
        b.i18n_ja = json.dumps(cur, ensure_ascii=False)
        nb += 1

    for Model in (models.ChatMessage, models.PastChatMessage):
        for m in db.query(Model).all():
            text = data["messages"].get(msg_key(m))
            if text and m.content_ja != text:
                m.content_ja = text
                nm += 1

    db.commit()
    db.close()
    print("복원: 도서 %d권 · 메시지 %d건" % (nb, nm))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "dump"
    if cmd == "dump":
        dump()
    elif cmd == "restore":
        restore()
    else:
        print(__doc__)
        sys.exit(1)
