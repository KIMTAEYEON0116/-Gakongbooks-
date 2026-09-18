# -*- coding: utf-8 -*-
"""모든 아카이브 도서를 진행 중인 독서방(D-10)으로 활성화하고 대화 메시지를 복원하는 스크립트"""
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database
import models

def activate_all():
    db = database.SessionLocal()
    try:
        now = models.get_kst_now()
        books = db.query(models.Book).all()
        count = 0
        first_user = db.query(models.User).first()
        fallback_user_id = first_user.id if first_user else 1

        for b in books:
            b.is_archived = False
            b.deadline_days = 10
            b.created_at = now
            count += 1

            # 아카이브되었던 PastChatMessage 대화들을 실시간 ChatMessage로 안전하게 복사
            past_msgs = db.query(models.PastChatMessage).filter(models.PastChatMessage.book_id == b.id).all()
            for pm in past_msgs:
                exists = db.query(models.ChatMessage).filter(
                    models.ChatMessage.book_id == b.id,
                    models.ChatMessage.content == pm.content
                ).first()
                if not exists:
                    # 유저가 실제로 존재하는지 확인
                    user_exists = db.query(models.User).filter(models.User.id == pm.user_id).first()
                    uid = pm.user_id if user_exists else fallback_user_id
                    
                    db.add(models.ChatMessage(
                        book_id=b.id,
                        user_id=uid,
                        content=pm.content,
                        content_ja=pm.content_ja,
                        reactions=pm.reactions,
                        created_at=pm.original_created_at or now,
                    ))

        db.commit()
        print(f"[완료] 총 {count}권의 도서가 모두 'D-10 (진행 중인 독서방)'으로 활성화되었습니다!")
    finally:
        db.close()

if __name__ == "__main__":
    activate_all()
