# -*- coding: utf-8 -*-
"""이미 저장된 일본어 번역의 용어를 화면 용어에 맞춘다.

화면 메뉴는 전부 '読書室'인데, 번역된 사회자 인사말과 종료 인사에는
'読書ルーム'·'読書部屋'이 섞여 있다. 일본 독자에게는 다른 곳처럼 읽힌다.
목차 장 번호('제 1장')도 함께 바로잡는다.

본문의 뜻은 건드리지 않고 용어만 바꾼다.
"""
import os
import sys

# scripts/ 안에서 실행해도 프로젝트 모듈을 찾도록 경로를 먼저 잡는다.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

import database
import main
import models

TERMS = [("読書ルーム", "読書室"), ("読書部屋", "読書室")]


def fix(text):
    if not isinstance(text, str) or not text:
        return text, False
    out = text
    for a, b in TERMS:
        out = out.replace(a, b)
    return out, out != text


db = database.SessionLocal()
books_changed = chats_changed = toc_changed = 0
try:
    for b in db.query(models.Book).all():
        raw = (b.i18n_ja or "").strip()
        if not raw:
            continue
        try:
            ja = json.loads(raw)
        except Exception:
            continue
        touched = False
        for k, v in list(ja.items()):
            if k == "immersion_data":
                continue
            nv, ch = fix(v)
            if ch:
                ja[k] = nv
                touched = True

        imm_raw = ja.get("immersion_data")
        if imm_raw:
            try:
                imm = json.loads(imm_raw) if isinstance(imm_raw, str) else dict(imm_raw)
            except Exception:
                imm = None
            if imm:
                toc = imm.get("table_of_contents") or []
                t2 = False
                for ch_item in toc:
                    if not isinstance(ch_item, dict):
                        continue
                    old = ch_item.get("chapter_number")
                    new = main.chapter_label_ja(old)
                    if new != old:
                        ch_item["chapter_number"] = new
                        t2 = True
                        toc_changed += 1
                    for key in ("title", "summary"):
                        nv, c2 = fix(ch_item.get(key))
                        if c2:
                            ch_item[key] = nv
                            t2 = True
                if t2:
                    imm["table_of_contents"] = toc
                    ja["immersion_data"] = json.dumps(imm, ensure_ascii=False)
                    touched = True

        if touched:
            b.i18n_ja = json.dumps(ja, ensure_ascii=False)
            books_changed += 1
            print("  책 %d 수정" % b.id)

    for Model, tag in ((models.ChatMessage, "진행중"), (models.PastChatMessage, "지난방")):
        for m in db.query(Model).all():
            nv, ch = fix(getattr(m, "content_ja", None))
            if ch:
                m.content_ja = nv
                chats_changed += 1
                print("  %s 채팅 #%s 수정" % (tag, m.id))

    db.commit()
    print("책 %d권 / 채팅 %d건 / 장 번호 %d칸 수정" % (books_changed, chats_changed, toc_changed))

    # 확인
    left = []
    for b in db.query(models.Book).all():
        v = b.i18n_ja or ""
        for a, _ in TERMS:
            if a in v:
                left.append("책%d:%s" % (b.id, a))
    for Model, tag in ((models.ChatMessage, "진행중"), (models.PastChatMessage, "지난방")):
        for m in db.query(Model).all():
            v = getattr(m, "content_ja", None) or ""
            for a, _ in TERMS:
                if a in v:
                    left.append("%s#%s:%s" % (tag, m.id, a))
    print("남은 흔들리는 표기: %s" % (left or "없음"))
finally:
    db.close()
