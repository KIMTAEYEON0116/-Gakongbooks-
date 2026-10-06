# -*- coding: utf-8 -*-
"""후보 도서 표에 i18n_ja 칸을 추가한다.

SQLAlchemy의 create_all은 이미 있는 표에 칸을 더해 주지 않는다.
운영 DB에는 직접 넣어야 한다. 이미 있으면 아무것도 하지 않는다.
"""
import os
import sys

# scripts/ 안에서 실행해도 프로젝트 모듈을 찾도록 경로를 먼저 잡는다.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text

import database

TABLE = "candidate_books"
COLUMN = "i18n_ja"

with database.engine.connect() as conn:
    rows = conn.execute(text(
        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :t AND COLUMN_NAME = :c"
    ), {"t": TABLE, "c": COLUMN}).fetchall()

    if rows:
        print("이미 있음 — 그대로 둔다: %s.%s" % (TABLE, COLUMN))
    else:
        conn.execute(text("ALTER TABLE %s ADD COLUMN %s TEXT NULL" % (TABLE, COLUMN)))
        conn.commit()
        print("추가함: %s.%s" % (TABLE, COLUMN))

    got = conn.execute(text(
        "SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE FROM INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :t AND COLUMN_NAME = :c"
    ), {"t": TABLE, "c": COLUMN}).fetchall()
    print("확인:", got)
