# -*- coding: utf-8 -*-
"""일본어 번역본을 기계적으로 점검한다.

일본어 화면에 한국어가 한 글자도 남으면 안 된다는 것이 이 프로젝트의 규칙이다.
번역을 새로 넣거나 고친 뒤에 이 스크립트를 돌려 규칙이 깨지지 않았는지 본다.

  python scripts/verify_ja.py

1단계 — 건별 점검
  번역 누락 / 한글 잔존 / 원문과 동일 / 길이 이상 / 숫자 누락 / 가나 부재

2단계 — 어긋남 점검
  번역 하나하나는 옳아도 표기가 갈리면 독자는 다른 인물로 읽는다.
  인물·용어 표기가 같은 책 안에서 일관된지, 존칭과 어미가 남았는지 본다.

알려진 오탐 세 가지 (고칠 것이 아니다)
  live#474  본문이 '@moderator'뿐이라 번역문과 원문이 같다.
  '손님'    존칭 검사의 '[가-힣]님' 규칙에 걸린다. 客이 맞는 번역이다.
  '지우려'  도서 39의 인물 '지우'가 아니라 동사 지우다이다. 消す가 맞다.
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(errors="replace")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database  # noqa: E402
import models    # noqa: E402
import main      # noqa: E402

RX_KANA = re.compile(r"[぀-ヿ]")

# 책마다 '이 낱말은 이렇게 적기로 했다'
# 도서 29의 켄지(ケンジ)와 도서 45의 겐지(ゲンジ)는 다른 인물이다.
# 한국어는 두 이름을 구분해 적으므로 일본어에서도 구분한다.
TERMS = {
    29: {"사쿠라": "サクラ", "켄지": "ケンジ"},
    36: {"아델": "アデル"},
    38: {"테오": "テオ", "그레고리": "グレゴリー", "단안경": "単眼鏡", "해도": "海図"},
    39: {"지우": "ジウ"},
    40: {"셀레나": "セレナ", "만년필": "万年筆"},
    41: {"엘리아스": "エリアス", "리벳": "リベット", "찻잔": "茶碗"},
    42: {"엘리사": "エリサ", "레오": "レオ", "서고": "書庫", "아틀라스": "アトラス"},
    43: {"은유": "ウンユ", "정우": "ジョンウ"},
    44: {"페더리": "フェザリー", "부엉": "ブオン"},
    45: {"유키": "ユキ", "겐지": "ゲンジ"},
    49: {"엘리샤": "エリシャ", "카일": "カイル"},
}

# 장르는 i18n_ja가 아니라 프론트의 GENRE_I18N 사전이 옮긴다. 여기서는 보지 않는다.
BOOK_FIELDS = ["title", "author", "synopsis", "tags", "memorable_quote",
               "endorsement_quote", "endorsement_attr", "closing_remark"]
NO_KANA_OK = ("tags", "author", "endorsement_attr")

db = database.SessionLocal()
mod = db.query(models.User).filter(models.User.is_bot == True).first()
problems = []


def add(label, why, sample):
    problems.append((label, why, (sample or "")[:44]))


def check_pair(label, src, dst, allow_no_kana=False):
    if not dst or not dst.strip():
        add(label, "번역 없음", src); return
    if main.has_hangul(dst):
        add(label, "한글 잔존 %s" % re.findall(r"[가-힣]+", dst)[:3], dst); return
    if src and dst.strip() == src.strip():
        add(label, "원문과 동일", dst); return
    if src:
        ratio = len(dst) / max(len(src), 1)
        if ratio < 0.5 or ratio > 2.5:
            add(label, "길이 %.2f배 (%d→%d)" % (ratio, len(src), len(dst)), dst)
        missing = set(re.findall(r"\d+", src)) - set(re.findall(r"\d+", dst))
        if missing:
            add(label, "숫자 누락 %s" % sorted(missing), dst)
    if not allow_no_kana and not RX_KANA.search(dst) and len(dst) > 6:
        add(label, "가나 없음(한자어를 그대로 둔 것일 수 있음)", dst)


counts = {}
for Model, tag in ((models.ChatMessage, "live"), (models.PastChatMessage, "past")):
    rows = db.query(Model).all()
    counts[tag] = len(rows)
    for m in rows:
        who = "사회자" if m.user_id == mod.id else "독자"
        label = "%s#%d(%s)" % (tag, m.id, who)
        src, dst = m.content or "", m.content_ja or ""
        check_pair(label, src, dst)
        if not dst:
            continue

        for ko, ja in TERMS.get(m.book_id, {}).items():
            if ko in src and ja not in dst:
                add(label, "표기 불일치: '%s' → '%s' 없음" % (ko, ja), dst)

        if re.search(r"[가-힣]님", src) and not re.search(r"さん|さま|様", dst):
            add(label, "존칭 누락", dst)

        for bad in ("입니다", "네요", "해요", "습니다"):
            if bad in dst:
                add(label, "한국어 어미 '%s'" % bad, dst)

books = db.query(models.Book).all()
counts["books"] = len(books)
for b in books:
    d = json.loads(b.i18n_ja or "{}")
    if not d:
        add("book#%d" % b.id, "i18n_ja 없음", b.title); continue
    for f in BOOK_FIELDS:
        src = getattr(b, f, None)
        if src:
            check_pair("book#%d.%s" % (b.id, f), src, d.get(f), allow_no_kana=f in NO_KANA_OK)

print("라이브 %d건 · 보관 %d건 · 도서 %d권" % (counts["live"], counts["past"], counts["books"]))
print("이상 %d건" % len(problems))
for label, why, sample in problems:
    print("   [!] %-22s %-42s %s" % (label, why, sample))
db.close()
sys.exit(0)
