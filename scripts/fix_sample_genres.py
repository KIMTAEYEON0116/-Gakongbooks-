# -*- coding: utf-8 -*-
"""샘플 책의 장르 표기를 내용에 맞게 바로잡는다.

초기 샘플 책 몇 권이 '에세이/비문학'으로 표기돼 있었지만 내용은 주인공과 사건이 있는
소설이다. 일본어 화면의 장르 라벨과 줄거리가 어긋나 보이므로 제목 기준으로 고친다.
같은 제목이 현재 책·후보·아카이브 어디에 있든 모두 바꾼다. 줄거리 오타 1건도 함께 고친다.

실행:  cd ~/-Gakongbooks- && PYTHONPATH=. venv/bin/python scripts/fix_sample_genres.py          # 미리 보기
       cd ~/-Gakongbooks- && PYTHONPATH=. venv/bin/python scripts/fix_sample_genres.py --apply  # 적용
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(errors="replace")

import database  # noqa: E402
import models    # noqa: E402

GENRE_FIX = {
    "깨진 렌즈가 비춘 잃어버린 항해": "판타지 모험",
    "닳아버린 시선에게 운명을 묻다": "드라마/성장소설",
    "셔터 소리, 어긋난 계절을 찍다": "드라마/성장소설",
    "낡은 렌즈가 품은 새벽의 망설임": "힐링/일상소설",
    "벚꽃 아래, 늙은 안경에 깃든 기다림": "힐링/일상소설",
}
TYPO_FIX = {"낡은 타자기은": "낡은 타자기는"}

APPLY = "--apply" in sys.argv
db = database.SessionLocal()
changed = 0

for model in (models.Book, models.CandidateBook):
    for row in db.query(model).all():
        new_genre = GENRE_FIX.get(row.title)
        if new_genre and row.genre != new_genre:
            print(f"[{model.__name__} {row.id}] {row.title}: {row.genre} -> {new_genre}")
            row.genre = new_genre
            changed += 1
        syn = row.synopsis or ""
        for old, new in TYPO_FIX.items():
            if old in syn:
                print(f"[{model.__name__} {row.id}] 줄거리 오타: {old} -> {new}")
                row.synopsis = syn.replace(old, new)
                changed += 1

# 남은 '에세이/비문학' 표기 중 허구 서사로 보이는 책을 알려만 준다(자동 변경하지 않음)
left = db.query(models.Book).filter(models.Book.genre == "에세이/비문학").all()
for b in left:
    print(f"[확인 필요] Book {b.id} {b.title}: 여전히 에세이/비문학")

print(f"변경 {changed}건" + ("" if APPLY else " (미리 보기, --apply 로 적용)"))
if APPLY and changed:
    db.commit()
    print("적용 완료")
db.close()
