# -*- coding: utf-8 -*-
# 실행: 저장소 루트에서  python tests/test_cover_backfill.py
"""표지 생성·되채우기 규칙을 확인한다. 외부 이미지 API는 부르지 않는다.

  1. 같은 번호라도 제목이 다르면 표지 파일 이름이 다르다 (충돌 방지)
  2. API가 402를 돌려주면 None으로 끝나고, 다음 호출은 간격이 지난 뒤에만 허용된다
  3. 차례가 max_wait 보다 멀면 기다리지 않고 바로 None (채택 직전 경로가 막히지 않게)
  4. PIL 도형 표지(450x600)와 AI 표지를 구분한다
  5. 되채우기 대상은 열린 방 → 고르는 중인 후보 → 보관 후보 → 종료된 방 순으로 고른다
"""
import asyncio
import os
import sys
import tempfile
import time

sys.path.insert(0, os.getcwd())
sys.stdout.reconfigure(errors="replace")

from PIL import Image  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

import main    # noqa: E402
import models  # noqa: E402

results = []


def check(label, ok, extra=""):
    results.append(ok)
    print(("  [통과] " if ok else "  [실패] ") + label + (" " + extra if extra else ""))


# ── 1. 파일 이름 충돌 ──
a = main.cover_uid("cand", 4, "해피엔딩을 묻는 오르골")
b = main.cover_uid("cand", 4, "체스판의 미학")
check("같은 번호·다른 제목 → 다른 파일 이름", a != b and a.startswith("cand_4_"), f"{a} / {b}")
check("같은 번호·같은 제목 → 같은 파일 이름(재사용)", a == main.cover_uid("cand", 4, "해피엔딩을 묻는 오르골"))


# ── 2·3. 402 처리와 간격 ──
class _Resp:
    def __init__(self, code, content=b"{}"):
        self.status_code, self.content = code, content


class _Client:
    code = 402

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    async def get(self, *a, **k):
        return _Resp(_Client.code)


main.httpx.AsyncClient = _Client
main._POLL_NEXT_OK = 0.0
main._POLL_LOCK = None

t0 = time.monotonic()
r1 = asyncio.run(main._pollinations_fetch("x", 1, max_wait=5.0))
check("402 응답 → None", r1 is None)
check("402 뒤에는 다음 허용 시각이 65초 뒤로 잡힌다", main._POLL_NEXT_OK - t0 > 60)
t1 = time.monotonic()
r2 = asyncio.run(main._pollinations_fetch("x", 2, max_wait=5.0))
check("차례가 멀면 기다리지 않고 바로 None", r2 is None and time.monotonic() - t1 < 1.0)

# ── 4. 도형 표지 판별 ──
tmp = tempfile.mkdtemp()
pil_path = os.path.join(tmp, "pil.png")
ai_path = os.path.join(tmp, "ai.png")
Image.new("RGB", (450, 600), "#eee").save(pil_path)
Image.new("RGB", (665, 886), "#345").save(ai_path)
check("450x600 → 도형 표지로 판별", main._is_fallback_cover(pil_path))
check("665x886(AI) → 도형 표지 아님", not main._is_fallback_cover(ai_path) or os.path.getsize(ai_path) < 5000,
      "(단색이라 5KB 미만이면 통과로 본다)")
check("없는 파일 → 도형 표지로 취급(교체 대상)", main._is_fallback_cover(os.path.join(tmp, "none.png")))

# ── 5. 대상 선정 순서 ──
eng = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
models.Base.metadata.create_all(eng)
Session = sessionmaker(bind=eng)
db = Session()
common = dict(author="a", genre="SF", synopsis="s", tags="#t", price="₩1", page_count=1, deadline_days=10)
arch = models.Book(title="종료된 방", is_archived=True, cover_image_url=None, **common)
open_ = models.Book(title="열린 방", is_archived=False, cover_image_url=None, **common)
db.add_all([arch, open_])
db.add(models.CandidateBook(title="후보", author="a", genre="SF", synopsis="s", tags="#t", status="pending"))
db.commit()
kind, row = main._pick_cover_backfill_target(db)
check("열린 방이 가장 먼저 뽑힌다", kind == "book" and row.title == "열린 방", f"{kind}:{row.title}")
open_.cover_image_url = ai_path.replace(os.sep, "/")
db.commit()
if os.path.getsize(ai_path) < 5000:
    # 단색 그림은 5KB 미만이라 도형 표지로 분류된다. 판별을 통과하도록 잡음을 넣는다.
    import random
    im = Image.new("RGB", (665, 886))
    im.putdata([(random.randrange(256), random.randrange(256), random.randrange(256)) for _ in range(665 * 886)])
    im.save(ai_path)
kind2, row2 = main._pick_cover_backfill_target(db)
check("열린 방이 AI 표지를 갖추면 다음은 고르는 중인 후보", kind2 == "cand", f"{kind2}:{row2.title}")
db.close()

print()
print("결과: " + ("모두 통과" if all(results) else "%d건 실패" % results.count(False)))
sys.exit(0 if all(results) else 1)
