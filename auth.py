"""
인증(누구인가) · 인가(무엇을 할 수 있는가) 계층.

엔드포인트는 여기서 제공하는 의존성만 사용한다:
  - get_current_user_id : 로그인 필수, user_id(int) 반환
  - get_current_user    : 로그인 필수, User 객체 반환
  - require_admin       : 관리자 필수, User 객체 반환
비밀번호 해싱/토큰 발급도 전부 이 모듈을 거치도록 해서 정책을 한곳에서 바꿀 수 있게 한다.
"""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import config
import database
import models

SECRET_KEY = config.JWT_SECRET_KEY
ALGORITHM = config.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

# OAuth2 스키마 정의 (토큰 자동 헤더 매핑용)
# 클라이언트로부터 'Authorization: Bearer <token>' 헤더를 파싱합니다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="로그인이 필요한 서비스입니다.",
    headers={"WWW-Authenticate": "Bearer"},
)


# ── 비밀번호 보안 해싱 (bcrypt) ──

def get_password_hash(password: str) -> str:
    """평문 비밀번호를 bcrypt 해시로 변환합니다."""
    salt = bcrypt.gensalt()
    # bcrypt는 바이트 입력을 받으므로 인코딩 및 디코딩 처리합니다.
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """평문 비밀번호가 저장된 해시 비밀번호와 일치하는지 비교 검증합니다."""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False


def set_password(user: "models.User", new_password: str) -> None:
    """
    비밀번호를 교체하고, 발급 시점이 더 이른 기존 토큰을 모두 무효화한다.
    (비밀번호 변경 · 임시 비밀번호 발급 등 모든 경로가 이 함수를 사용해야 한다.)
    """
    user.password_hash = get_password_hash(new_password)
    user.password_changed_at = models.get_kst_now()


# ── JWT 토큰 발급 및 검증 ──

def _to_epoch(dt: datetime) -> int:
    """KST naive datetime을 UTC epoch 초로 변환한다 (DB 저장 형식이 KST naive이므로)."""
    return int(dt.replace(tzinfo=timezone(timedelta(hours=9))).timestamp())


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """회원의 ID 또는 이메일을 인코딩하여 JWT 액세스 토큰을 생성합니다."""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    # iat: 비밀번호 변경 시각과 비교해 옛 토큰을 걸러내는 데 사용한다.
    to_encode.update({"exp": expire, "iat": now})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db),
) -> "models.User":
    """
    JWT를 검증하고 실제 User 레코드를 반환합니다.
    토큰이 없거나 위조/만료됐거나, 발급 이후 비밀번호가 바뀌었거나,
    계정이 삭제된 경우 401을 발생시킵니다.
    """
    if not token:
        raise _CREDENTIALS_EXCEPTION

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise _CREDENTIALS_EXCEPTION

    user_id = payload.get("user_id")
    if user_id is None:
        raise _CREDENTIALS_EXCEPTION

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        # 탈퇴한 계정의 토큰은 만료 전이라도 통과시키지 않는다.
        raise _CREDENTIALS_EXCEPTION

    issued_at = payload.get("iat")
    if user.password_changed_at and issued_at is not None:
        # 비밀번호 변경 이전에 발급된 토큰은 무효 (탈취 대응 수단)
        if int(issued_at) < _to_epoch(user.password_changed_at):
            raise _CREDENTIALS_EXCEPTION

    return user


def get_current_user_id(user: "models.User" = Depends(get_current_user)) -> int:
    """로그인한 사용자의 id만 필요할 때 사용하는 얇은 래퍼."""
    return user.id


# ── 비밀번호 재설정 토큰 ──
# 규칙: 원문 토큰은 메일로만 나가고, DB에는 해시만 저장한다. 1회 사용 후 즉시 폐기한다.

def _hash_reset_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def issue_reset_token(user: "models.User") -> str:
    """재설정 토큰을 발급하고 해시를 사용자 레코드에 기록한다. 원문 토큰을 반환한다."""
    raw_token = secrets.token_urlsafe(32)
    user.reset_token_hash = _hash_reset_token(raw_token)
    user.reset_token_expires_at = models.get_kst_now() + timedelta(
        minutes=config.PASSWORD_RESET_TTL_MINUTES
    )
    return raw_token


def consume_reset_token(db: Session, raw_token: str) -> "models.User":
    """
    토큰을 검증하고 해당 사용자를 반환하며 토큰을 폐기한다.
    유효하지 않거나 만료된 경우 400을 발생시킨다.
    """
    invalid = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="재설정 링크가 유효하지 않거나 만료되었습니다. 다시 요청해 주세요.",
    )
    if not raw_token:
        raise invalid

    user = (
        db.query(models.User)
        .filter(models.User.reset_token_hash == _hash_reset_token(raw_token))
        .first()
    )
    if not user or not user.reset_token_expires_at:
        raise invalid
    if user.reset_token_expires_at < models.get_kst_now():
        clear_reset_token(user)
        db.commit()
        raise invalid
    return user


def clear_reset_token(user: "models.User") -> None:
    user.reset_token_hash = None
    user.reset_token_expires_at = None


def require_admin(user: "models.User" = Depends(get_current_user)) -> "models.User":
    """관리자 전용 엔드포인트에서 사용하는 인가 의존성."""
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요한 작업입니다.",
        )
    return user
