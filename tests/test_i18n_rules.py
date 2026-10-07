# -*- coding: utf-8 -*-
# 실행: 저장소 루트에서  python tests/test_i18n_rules.py
"""일본어 화면을 떠받치는 규칙들을 고정한다.

이 프로젝트의 약속은 하나다 — 일본어 화면에 한국어가 한 글자도 남지 않는다.
그 약속을 지키는 장치들이 여럿인데, 하나씩 조용히 어긋난 적이 있다.

  · 장 번호만 '제 1장'으로 남았다 (목차는 제목·요약만 번역했기 때문)
  · 응답 문구가 늘 한국어였다 (예외를 모듈 읽을 때 한 번 만들어 둬서)
  · 번역이 반만 된 책이 되채우기 대상에서 빠졌다 (비어 있지는 않아서)
  · 조사가 받침과 어긋났다 ('등불와')

외부 호출 없이 순수 함수만 확인하므로 API 키도 DB도 필요 없다.
"""
import os
import sys

sys.path.insert(0, os.getcwd())
sys.stdout.reconfigure(errors="replace")

import fallback_books  # noqa: E402
import i18n            # noqa: E402
import main            # noqa: E402

ok = True


def expect(label, cond, extra=""):
    global ok
    if not cond:
        ok = False
    print("%s %s %s" % ("OK  " if cond else "FAIL", label, extra))


# ── 1) 장 번호 표기 ──
expect("'제 1장' → '第1章'", main.chapter_label_ja("제 1장") == "第1章")
expect("띄어쓰기 없어도 변환", main.chapter_label_ja("제2장") == "第2章")
expect("두 자리 장도 변환", main.chapter_label_ja("제 10장") == "第10章")
expect("에필로그 → エピローグ", main.chapter_label_ja("에필로그") == "エピローグ")
expect("이미 일본어면 그대로", main.chapter_label_ja("第3章") == "第3章")
expect("규칙 밖의 값은 그대로", main.chapter_label_ja("프롤로그 2부") == "프롤로그 2부")

# ── 2) 응답 문구의 언어 ──
token = i18n.set_request_lang("ja")
expect("일본어 요청 → 일본어 문구", i18n.m("한국어", "日本語") == "日本語")
i18n.reset_request_lang(token)

token = i18n.set_request_lang("ko")
expect("한국어 요청 → 한국어 문구", i18n.m("한국어", "日本語") == "한국어")
i18n.reset_request_lang(token)

token = i18n.set_request_lang("")
expect("헤더가 없으면 일본어", i18n.m("한국어", "日本語") == "日本語")
i18n.reset_request_lang(token)

token = i18n.set_request_lang("fr")
expect("모르는 값이어도 일본어", i18n.m("한국어", "日本語") == "日本語")
i18n.reset_request_lang(token)


# ── 3) 번역이 '반만' 된 책을 알아보는가 ──
class FakeBook:
    """ja_missing_fields가 보는 자리만 흉내 낸다."""

    def __init__(self, i18n_ja, **fields):
        self.i18n_ja = i18n_ja
        self.immersion_data = fields.pop("immersion_data", None)
        for k in main.BOOK_TRANSLATABLE_FIELDS:
            setattr(self, k, fields.get(k))


full = '{"title": "題", "synopsis": "あらすじ"}'
expect("필요한 칸이 다 있으면 빠진 것 없음",
       main.ja_missing_fields(FakeBook(full, title="제목", synopsis="줄거리")) == [])
expect("한 칸이 비면 그 칸을 집어냄",
       main.ja_missing_fields(FakeBook('{"title": "題"}', title="제목", synopsis="줄거리")) == ["synopsis"])
expect("i18n_ja가 아예 없으면 전부 빠진 것",
       set(main.ja_missing_fields(FakeBook(None, title="제목", synopsis="줄거리"))) == {"title", "synopsis"})

# 목차에 한글이 남아 있으면 미완성으로 본다 (예전에는 길이만 봐서 놓쳤다)
src_toc = '{"table_of_contents": [{"chapter_number": "제 1장", "title": "가", "summary": "나"}]}'
dirty_toc = '{"title": "題", "immersion_data": "{\\"table_of_contents\\": [{\\"chapter_number\\": \\"第1章\\", \\"title\\": \\"タイトル\\", \\"summary\\": \\"한국어가 남음\\"}]}"}'
expect("목차에 한글이 남으면 미완성",
       "immersion_data" in main.ja_missing_fields(
           FakeBook(dirty_toc, title="제목", immersion_data=src_toc)))

clean_toc = '{"title": "題", "immersion_data": "{\\"table_of_contents\\": [{\\"chapter_number\\": \\"第1章\\", \\"title\\": \\"タイトル\\", \\"summary\\": \\"ようやく日本語\\"}]}"}'
expect("목차가 온전하면 통과",
       "immersion_data" not in main.ja_missing_fields(
           FakeBook(clean_toc, title="제목", immersion_data=src_toc)))

# ── 4) 조사가 받침을 따라가는가 ──
expect("받침 있으면 '과'", fallback_books._particles("등불", "c")["wa_c"] == "과")
expect("받침 없으면 '와'", fallback_books._particles("모자", "c")["wa_c"] == "와")
expect("받침 있으면 '을'", fallback_books._particles("등불", "c")["eul_c"] == "을")
expect("받침 없으면 '를'", fallback_books._particles("모자", "c")["eul_c"] == "를")
expect("받침 있으면 '이라는'", fallback_books._particles("등불", "c")["ira_c"] == "이라는")
expect("받침 없으면 '라는'", fallback_books._particles("모자", "c")["ira_c"] == "라는")

# ── 5) 대체 자료가 두 언어로 성한가 ──
HANGUL = tuple("가힣")


def has_hangul(text):
    return any("가" <= ch <= "힣" for ch in str(text))


def has_kana(text):
    return any("぀" <= ch <= "ヿ" for ch in str(text))


bad_ja, bad_ko, bad_fmt, bad_pair = [], [], [], []
for genre, langs in fallback_books.GENRE_FALLBACKS.items():
    ko, ja = langs.get("ko"), langs.get("ja")
    if not ko or not ja:
        bad_pair.append(genre)
        continue
    if len(ko["abstract"]) != len(ja["abstract"]) or len(ko["concrete"]) != len(ja["concrete"]):
        bad_pair.append(genre)
    kw_ko, kw_ja = fallback_books.make_keywords(genre)
    for key in ("title", "synopsis", "endorsement", "review"):
        for tpl in ja[key]:
            try:
                out = tpl.format(**kw_ja)
            except Exception:
                bad_fmt.append("%s/ja/%s" % (genre, key))
                continue
            if has_hangul(out):
                bad_ja.append("%s/%s" % (genre, key))
        for tpl in ko[key]:
            try:
                out = tpl.format(**kw_ko)
            except Exception:
                bad_fmt.append("%s/ko/%s" % (genre, key))
                continue
            if has_kana(out):
                bad_ko.append("%s/%s" % (genre, key))

expect("장르 9종이 모두 있다", len(fallback_books.GENRE_FALLBACKS) == 9,
       "(%d종)" % len(fallback_books.GENRE_FALLBACKS))
expect("두 언어의 낱말 수가 짝이 맞는다", not bad_pair, str(bad_pair[:3]))
expect("자리표가 모두 채워진다", not bad_fmt, str(bad_fmt[:3]))
expect("일본어 문장틀에 한글이 없다", not bad_ja, str(bad_ja[:3]))
expect("한국어 문장틀에 가나가 없다", not bad_ko, str(bad_ko[:3]))

# 실제 장르 이름으로 조회된다 (예전에는 키가 달라 엉뚱한 장르의 문장틀을 썼다)
for g in ("SF/스페이스 탐험", "추리/미스터리", "힐링/일상소설", "로맨스 판타지"):
    expect("'%s' 전용 자료가 있다" % g, g in fallback_books.GENRE_FALLBACKS)

# 작가 이름은 두 표기가 함께 나온다
for _ in range(20):
    nation, nation_ja, name_ko, name_ja = fallback_books.make_author()
    if has_hangul(name_ja) or not name_ko or not name_ja:
        expect("작가 이름의 일본어 표기에 한글이 없다", False, "(%s / %s)" % (name_ko, name_ja))
        break
else:
    expect("작가 이름의 일본어 표기에 한글이 없다", True)

print("결과:", "전부 통과" if ok else "실패 있음")
sys.exit(0 if ok else 1)
