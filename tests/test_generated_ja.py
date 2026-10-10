# -*- coding: utf-8 -*-
# 실행: 저장소 루트에서  python tests/test_generated_ja.py
"""생성 단계에서 함께 받은 일본어 블록을 저장용으로 다듬는 규칙을 확인한다.

모델이 돌려주는 ja 블록은 완벽하지 않다. 한글이 섞이거나, 질문 수가 다르거나,
목차가 모자랄 수 있다. 그런 칸만 버리고 나머지는 살려야 한다(전체를 버리면
네 칸짜리 시절로 돌아간다). 외부 호출은 없다.
"""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
sys.stdout.reconfigure(errors="replace")

import main  # noqa: E402

results = []


def check(label, ok, extra=""):
    results.append(ok)
    print(("  [통과] " if ok else "  [실패] ") + label + (" " + extra if extra else ""))


src = {
    "title": "깨진 렌즈가 비춘 항해", "author": "에단 리", "synopsis": "줄거리",
    "tags": ["#항해", "#렌즈", "#비극", "#AI가공"],
    "additional_questions": ["Q. 하나?", "Q. 둘?"],
    "characters": "에단 — 주인공|서연 — 조력자",
    "immersion_data": {"table_of_contents": [
        {"chapter_number": "제 1장", "title": "출항", "pages": "9 - 60", "summary": "요약1"},
        {"chapter_number": "제 2장", "title": "폭풍", "pages": "61 - 140", "summary": "요약2"},
    ]},
}

good = {
    "title": "砕けたレンズが映す航海", "author": "イーサン・リー", "synopsis": "あらすじ",
    "tags": ["#航海", "#レンズ", "#悲劇", "#AI創作"],
    "endorsement_quote": "息をのむ一冊。", "endorsement_attr": "文芸評論家",
    "publisher_review": "書評", "opening_line": "その夜。", "memorable_quote": "名台詞。",
    "core_dilemma": "Q. 真実と向き合いますか。",
    "additional_questions": ["Q. ひとつ目は。", "Q. ふたつ目は。"],
    "characters": "イーサン — 主人公|ソヨン — 協力者",
    "table_of_contents": [{"title": "出航", "summary": "要約1"}, {"title": "嵐", "summary": "要約2"}],
}

out = json.loads(main.build_candidate_i18n_ja(good, src))
check("정상 블록: 13칸이 모두 저장된다 (목차는 immersion_data로)",
      all(k in out for k in ("title", "author", "synopsis", "tags", "endorsement_quote", "endorsement_attr",
                             "publisher_review", "opening_line", "memorable_quote", "core_dilemma",
                             "additional_questions", "characters", "immersion_data")),
      str(sorted((set(good) | {"immersion_data"}) - set(out))))
check("추천인은 '— 직업（匿名）' 꼴로 맞춘다", out["endorsement_attr"] == "— 文芸評論家（匿名）", out["endorsement_attr"])
check("추가 질문은 '|'로 잇는다", out["additional_questions"] == "Q. ひとつ目は。|Q. ふたつ目は。")
toc = json.loads(out["immersion_data"])["table_of_contents"]
check("목차는 장 번호를 第n章으로, 쪽수는 원문대로 둔다",
      toc[0]["chapter_number"] == "第1章" and toc[0]["pages"] == "9 - 60" and toc[1]["title"] == "嵐", str(toc[0]))

bad = dict(good)
bad["synopsis"] = "あらすじに 한글 이 섞임"
bad["additional_questions"] = ["Q. ひとつだけ。"]
bad["characters"] = "イーサン — 主人公"
bad["table_of_contents"] = [{"title": "出航", "summary": "要約1"}]
out2 = json.loads(main.build_candidate_i18n_ja(bad, src))
check("한글이 섞인 칸만 버린다 (제목 등은 살린다)", "synopsis" not in out2 and out2.get("title") == good["title"])
check("질문 수가 다르면 그 칸을 버린다", "additional_questions" not in out2)
check("인물 수가 다르면 그 칸을 버린다", "characters" not in out2)
check("목차가 모자라면 목차를 넣지 않는다", "immersion_data" not in out2)

check("블록이 없으면 None", main.build_candidate_i18n_ja(None, src) is None)
check("쓸 칸이 하나도 없으면 None", main.build_candidate_i18n_ja({"title": "한글 제목"}, src) is None)

print()
print("결과: " + ("모두 통과" if all(results) else "%d건 실패" % results.count(False)))
sys.exit(0 if all(results) else 1)
