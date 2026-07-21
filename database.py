import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse

# .env 파일 절대경로로 명시적 로드 (uvicorn reloader 환경에서도 안정적으로 동작)
_env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=_env_path, override=True)

# 데이터베이스 연결 URL 획득
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # .env 파일이 없는 경우 SQLite로 임시 전환 (비밀번호 하드코딩 금지)
    DATABASE_URL = "sqlite:///./gakong.db"

# 안전하게 charset 매개변수 주입
if "mysql" in DATABASE_URL.lower() and "charset=" not in DATABASE_URL.lower():
    if "?" in DATABASE_URL:
        DATABASE_URL += "&charset=utf8mb4"
    else:
        DATABASE_URL += "?charset=utf8mb4"

print(f"\n[DB] 연결 시도: {DATABASE_URL[:DATABASE_URL.index('@')+1]}***")

use_sqlite = False
if "sqlite" in DATABASE_URL.lower():
    use_sqlite = True
else:
    import pymysql
    try:
        parsed = urlparse(DATABASE_URL)
        username = parsed.username or "root"
        password = parsed.password or ""
        hostname = parsed.hostname or "localhost"
        port = parsed.port or 3306
        db_name = parsed.path.lstrip('/') or "gakong_db"

        # MySQL 연결 테스트 및 DB 자동 생성
        conn = pymysql.connect(
            host=hostname,
            user=username,
            password=password,
            port=port,
            connect_timeout=5
        )
        with conn.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
                f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
        conn.close()
        print(f"[DB] MySQL 연결 성공! → {hostname}:{port}/{db_name}\n")
    except Exception as e:
        print(f"\n[!] MySQL 연결 실패 ({e})")
        print(f"[!] 로컬 SQLite(gakong.db)로 임시 전환합니다.\n")
        DATABASE_URL = "sqlite:///./gakong.db"
        use_sqlite = True

# SQLAlchemy Engine 생성
if use_sqlite:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_recycle=3600,
        pool_pre_ping=True
    )

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 정의 시 상속받을 Base 클래스
Base = declarative_base()

# FastAPI 엔드포인트에서 사용할 DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
