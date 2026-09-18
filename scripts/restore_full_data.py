# -*- coding: utf-8 -*-
"""로컬 DB의 모든 도서/메시지 데이터를 덤프하고 새 서버(SQLite 등)에 복원하는 스크립트"""
import io
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database
import models

BACKUP_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "data", "full_backup.json")


def dump_all():
    db = database.SessionLocal()
    try:
        # 1. Books
        books_data = []
        for b in db.query(models.Book).all():
            books_data.append({
                "id": b.id,
                "title": b.title,
                "author": b.author,
                "genre": b.genre,
                "synopsis": b.synopsis,
                "tags": b.tags,
                "price": b.price,
                "color": b.color,
                "cover_image_url": b.cover_image_url,
                "endorsement_quote": b.endorsement_quote,
                "endorsement_attr": b.endorsement_attr,
                "publisher_review": b.publisher_review,
                "opening_line": b.opening_line,
                "memorable_quote": b.memorable_quote,
                "core_dilemma": b.core_dilemma,
                "additional_questions": b.additional_questions,
                "characters": b.characters,
                "page_count": b.page_count,
                "immersion_data": b.immersion_data,
                "closing_remark": b.closing_remark,
                "i18n_ja": b.i18n_ja,
                "deadline_days": b.deadline_days,
                "is_archived": b.is_archived,
                "created_at": b.created_at.isoformat() if b.created_at else None,
            })

        # 2. PastChatMessage (아카이브된 채팅 메시지)
        past_msgs_data = []
        for m in db.query(models.PastChatMessage).all():
            past_msgs_data.append({
                "book_id": m.book_id,
                "user_id": m.user_id,
                "user_nickname": m.user_nickname,
                "content": m.content,
                "content_ja": m.content_ja,
                "reply_to_id": m.reply_to_id,
                "reply_to_user": m.reply_to_user,
                "reply_to_content": m.reply_to_content,
                "reactions": m.reactions,
                "original_created_at": m.original_created_at.isoformat() if m.original_created_at else None,
                "archived_at": m.archived_at.isoformat() if m.archived_at else None,
            })

        # 3. ChatMessage (현재 활성 채팅 메시지)
        active_msgs_data = []
        for m in db.query(models.ChatMessage).all():
            active_msgs_data.append({
                "book_id": m.book_id,
                "user_id": m.user_id,
                "content": m.content,
                "content_ja": m.content_ja,
                "reply_to_id": m.reply_to_id,
                "reactions": m.reactions,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            })

        payload = {
            "books": books_data,
            "past_chat_messages": past_msgs_data,
            "chat_messages": active_msgs_data,
        }

        os.makedirs(os.path.dirname(BACKUP_PATH), exist_ok=True)
        with io.open(BACKUP_PATH, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        print(f"[성공] 도서 {len(books_data)}권, 아카이브 메시지 {len(past_msgs_data)}건, 활성 메시지 {len(active_msgs_data)}건 백업 완료 -> {BACKUP_PATH}")
    finally:
        db.close()


def restore_all():
    if not os.path.exists(BACKUP_PATH):
        print(f"[에러] 백업 파일이 없습니다: {BACKUP_PATH}")
        return

    with io.open(BACKUP_PATH, "r", encoding="utf-8") as f:
        payload = json.load(f)

    db = database.SessionLocal()
    try:
        models.Base.metadata.create_all(bind=database.engine)

        books_data = payload.get("books", [])
        book_id_map = {}

        for b_data in books_data:
            existing = db.query(models.Book).filter(models.Book.title == b_data["title"]).first()
            if not existing:
                created_at = datetime.fromisoformat(b_data["created_at"]) if b_data.get("created_at") else datetime.utcnow()
                
                new_book = models.Book(
                    title=b_data.get("title"),
                    author=b_data.get("author"),
                    genre=b_data.get("genre"),
                    synopsis=b_data.get("synopsis"),
                    tags=b_data.get("tags"),
                    price=b_data.get("price", "₩14,000"),
                    color=b_data.get("color", "#7b5fb8"),
                    cover_image_url=b_data.get("cover_image_url"),
                    endorsement_quote=b_data.get("endorsement_quote"),
                    endorsement_attr=b_data.get("endorsement_attr"),
                    publisher_review=b_data.get("publisher_review"),
                    opening_line=b_data.get("opening_line"),
                    memorable_quote=b_data.get("memorable_quote"),
                    core_dilemma=b_data.get("core_dilemma"),
                    additional_questions=b_data.get("additional_questions"),
                    characters=b_data.get("characters"),
                    page_count=b_data.get("page_count"),
                    immersion_data=b_data.get("immersion_data"),
                    closing_remark=b_data.get("closing_remark"),
                    i18n_ja=b_data.get("i18n_ja"),
                    deadline_days=b_data.get("deadline_days", 10),
                    is_archived=b_data.get("is_archived", False),
                    created_at=created_at,
                )
                db.add(new_book)
                db.flush()
                book_id_map[b_data["id"]] = new_book.id
            else:
                existing.i18n_ja = b_data.get("i18n_ja") or existing.i18n_ja
                existing.is_archived = b_data.get("is_archived", existing.is_archived)
                existing.closing_remark = b_data.get("closing_remark") or existing.closing_remark
                existing.memorable_quote = b_data.get("memorable_quote") or existing.memorable_quote
                existing.characters = b_data.get("characters") or existing.characters
                existing.core_dilemma = b_data.get("core_dilemma") or existing.core_dilemma
                existing.cover_image_url = b_data.get("cover_image_url") or existing.cover_image_url
                book_id_map[b_data["id"]] = existing.id

        db.commit()

        # 과거 아카이브 메시지 복원
        past_msgs = payload.get("past_chat_messages", [])
        for m in past_msgs:
            target_book_id = book_id_map.get(m["book_id"])
            if not target_book_id:
                continue
            exists = db.query(models.PastChatMessage).filter(
                models.PastChatMessage.book_id == target_book_id,
                models.PastChatMessage.content == m["content"]
            ).first()
            if not exists:
                orig_created = datetime.fromisoformat(m["original_created_at"]) if m.get("original_created_at") else datetime.utcnow()
                arch_at = datetime.fromisoformat(m["archived_at"]) if m.get("archived_at") else datetime.utcnow()
                db.add(models.PastChatMessage(
                    book_id=target_book_id,
                    user_id=m.get("user_id", 1),
                    user_nickname=m.get("user_nickname", "독자"),
                    content=m.get("content"),
                    content_ja=m.get("content_ja"),
                    reply_to_id=m.get("reply_to_id"),
                    reply_to_user=m.get("reply_to_user"),
                    reply_to_content=m.get("reply_to_content"),
                    reactions=m.get("reactions"),
                    original_created_at=orig_created,
                    archived_at=arch_at,
                ))

        # 활성 채팅 메시지도 복원
        active_msgs = payload.get("chat_messages", [])
        for m in active_msgs:
            target_book_id = book_id_map.get(m["book_id"])
            if not target_book_id:
                continue
            exists = db.query(models.ChatMessage).filter(
                models.ChatMessage.book_id == target_book_id,
                models.ChatMessage.content == m["content"]
            ).first()
            if not exists:
                created_at = datetime.fromisoformat(m["created_at"]) if m.get("created_at") else datetime.utcnow()
                db.add(models.ChatMessage(
                    book_id=target_book_id,
                    user_id=m.get("user_id", 1),
                    content=m.get("content"),
                    content_ja=m.get("content_ja"),
                    reply_to_id=m.get("reply_to_id"),
                    reactions=m.get("reactions"),
                    created_at=created_at,
                ))

        db.commit()
        total_books = db.query(models.Book).count()
        print(f"[성공] 도서 {total_books}권 및 아카이브/채팅 데이터 전체 복원 완료!")
    finally:
        db.close()


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "dump"
    if action == "dump":
        dump_all()
    elif action == "restore":
        restore_all()
    else:
        print("사용법: python scripts/restore_full_data.py [dump|restore]")
