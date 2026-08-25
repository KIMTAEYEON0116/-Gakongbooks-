"""
요청 단위 보안 장치 모음 (레이트리밋 · 보안 헤더 · 클라이언트 IP 추출).

엔드포인트마다 임시 dict로 시도 횟수를 세는 코드를 복사하면 정책이 제각각이 되므로,
슬라이딩 윈도우 제한기를 하나만 두고 각 용도별로 인스턴스를 만들어 재사용한다.
"""

import threading
import time
from typing import Dict, List

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimiter:
    """
    (키 → 최근 시도 시각) 슬라이딩 윈도우 제한기.

    주의: 프로세스 메모리에만 저장되므로 워커를 여러 개 띄우거나 재시작하면 초기화된다.
    다중 워커로 운영할 계획이라면 이 클래스의 _hits 저장소만 Redis 등으로 교체하면 된다.
    """

    def __init__(self, max_attempts: int, window_seconds: int, message: str):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self.message = message
        self._hits: Dict[str, List[float]] = {}
        self._lock = threading.Lock()

    def _prune(self, key: str, now: float) -> List[float]:
        recent = [t for t in self._hits.get(key, []) if now - t < self.window_seconds]
        if recent:
            self._hits[key] = recent
        else:
            self._hits.pop(key, None)
        return recent

    def check(self, key: str) -> None:
        """한도를 넘었으면 429를 발생시킨다. (시도를 기록하지는 않는다)"""
        with self._lock:
            recent = self._prune(key, time.time())
            if len(recent) >= self.max_attempts:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=self.message.format(minutes=max(1, self.window_seconds // 60)),
                )

    def record(self, key: str) -> None:
        """실패(또는 소비) 1회를 기록한다."""
        with self._lock:
            now = time.time()
            self._prune(key, now)
            self._hits.setdefault(key, []).append(now)

    def reset(self, key: str) -> None:
        """성공 시 기록을 비운다."""
        with self._lock:
            self._hits.pop(key, None)

    def hit(self, key: str) -> None:
        """한도 확인과 기록을 한 번에 수행한다 (성공/실패 구분이 없는 용도)."""
        self.check(key)
        self.record(key)


def client_ip(request: Request) -> str:
    """
    클라이언트 IP를 추출한다.
    리버스 프록시 뒤에서 운영한다면 프록시가 X-Forwarded-For를 신뢰 가능하게 세팅해야 한다.
    """
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


# 브라우저 측 방어선. XSS가 하나 뚫려도 피해 범위를 줄여준다.
# script-src에 'unsafe-inline'이 남아 있는 이유: 템플릿과 books.js가 인라인 onclick 핸들러를
# 사용하고 있어서다. 인라인 핸들러를 걷어내면 이 항목을 제거할 수 있다.
_CSP = (
    "default-src 'self'; "
    "img-src 'self' data: https:; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com data:; "
    "script-src 'self' 'unsafe-inline'; "
    "connect-src 'self'; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'self'"
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """모든 응답에 공통 보안 헤더를 부착한다."""

    def __init__(self, app, is_production: bool = False):
        super().__init__(app)
        self.is_production = is_production

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers.setdefault("Content-Security-Policy", _CSP)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        if self.is_production:
            # HTTPS로 서비스할 때만 의미가 있으므로 운영에서만 부착한다.
            response.headers.setdefault(
                "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
            )
        return response
