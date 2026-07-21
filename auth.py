import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 환경변수 설정 읽기
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "gakong_super_secure_secret_key_2026")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# OAuth2 스키마 정의 (토큰 자동 헤더 매핑용)
# 클라이언트로부터 'Authorization: Bearer <token>' 헤더를 파싱합니다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


# ── 비밀번호 보안 해싱 (bcrypt) ──

def get_password_hash(password: str) -> str:
    """
    평문 비밀번호를 bcrypt 해시로 변환합니다.
    """
    salt = bcrypt.gensalt()
    # bcrypt는 바이트 입력을 받으므로 인코딩 및 디코딩 처리합니다.
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    평문 비밀번호가 저장된 해시 비밀번호와 일치하는지 비교 검증합니다.
    """
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False


# ── JWT 토큰 발급 및 검증 ──

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    회원의 ID 또는 이메일을 인코딩하여 JWT 액세스 토큰을 생성합니다.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user_id(token: Optional[str] = Depends(oauth2_scheme)) -> int:
    """
    API 요청 헤더의 JWT 토큰을 검증하고, 유효한 경우 user_id를 반환합니다.
    비로그인 상태이거나 유효하지 않은 경우 401 Unauthorized 에러를 발생시킵니다.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="로그인이 필요한 서비스입니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception

    try:
        # JWT 디코딩
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return user_id
    except jwt.PyJWTError:
        raise credentials_exception
