"""
애플리케이션 설정 단일 진입점.

환경변수를 읽는 코드가 여기저기 흩어지면 "이 값이 없으면 어떻게 되는가"를
파일마다 다르게 처리하게 되어 보안 사고로 이어진다. 모든 설정은 이 모듈에서만
읽고, 나머지 코드는 `import config` 후 상수를 참조한다.

핵심 규칙:
  - 운영(APP_ENV=production)에서 필수 시크릿이 비어 있으면 즉시 기동 실패한다.
  - 개발 환경에서만 편의를 위한 임시 기본값을 허용하고, 콘솔에 경고를 남긴다.
"""

import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

# .env는 이 모듈에서 딱 한 번만 로드한다 (uvicorn reloader 환경에서도 안정적이도록 절대경로 사용)
_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=True)


APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
_VALID_ENVS = ("development", "production")
if APP_ENV not in _VALID_ENVS:
    # 'prod', 'PRODUCTON' 같은 오타가 조용히 개발 모드로 떨어지면
    # 개발용 시크릿·문서 노출·완화된 CORS가 그대로 운영에 나간다. 차라리 기동을 막는다.
    raise RuntimeError(
        f"[치명] APP_ENV 값이 올바르지 않습니다: {APP_ENV!r} "
        f"(허용: {', '.join(_VALID_ENVS)})"
    )
IS_PRODUCTION = APP_ENV == "production"


class ConfigError(RuntimeError):
    """필수 설정이 누락되어 안전하게 기동할 수 없을 때 발생."""


def _get(name: str, default: str = "") -> str:
    return (os.getenv(name) or default).strip()


def _get_int(name: str, default: int) -> int:
    try:
        return int(_get(name, str(default)))
    except ValueError:
        print(f"[config] {name} 값이 정수가 아니어서 기본값 {default}을 사용합니다.")
        return default


def require_secret(name: str, dev_default: str, purpose: str) -> str:
    """
    시크릿을 읽는다. 운영에서는 미설정 시 기동을 중단하고,
    개발에서는 경고와 함께 임시 기본값을 사용한다.
    """
    value = _get(name)
    if value:
        return value
    if IS_PRODUCTION:
        raise ConfigError(
            f"[치명] {name}가 설정되지 않았습니다. {purpose}\n"
            f"       APP_ENV=production 에서는 반드시 .env에 {name}를 지정해야 합니다."
        )
    print(f"\n[!] 경고: {name} 미설정 → 이번 기동에만 쓰는 임시값을 생성했습니다. {purpose}")
    print(f"[!] 운영 배포 전 .env에 {name}를 반드시 설정하세요.\n")
    # 개발용 대체값은 소스에 고정하지 않고 매 기동 새로 만든다.
    # 고정 문자열이면 저장소를 본 사람이 그대로 토큰을 위조할 수 있고,
    # 실수로 운영에 그 상태가 나가도 눈치채기 어렵다.
    # (부작용: 서버를 재시작하면 기존 로그인 토큰이 무효가 된다 — 개발 중에는 오히려 안전한 쪽)
    return dev_default or secrets.token_urlsafe(32)


# ── 인증/토큰 ──
JWT_SECRET_KEY = require_secret(
    "JWT_SECRET_KEY",
    dev_default="",  # 비워두면 매 기동 난수를 생성한다
    purpose="이 값을 아는 사람은 누구나 로그인 토큰을 위조할 수 있습니다.",
)
JWT_ALGORITHM = _get("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = _get_int("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)

# ── 운영자 계정 ──
# 이 프로젝트의 유일한 운영자(사람). 기동 시 이 계정에만 관리자 권한을 부여하고,
# 다른 계정에 남아 있는 관리자 권한은 회수한다.
# 관리자 권한을 가질 유일한 계정.
#
# 저장소에 실제 이메일을 기본값으로 박아두지 않는다. 그 계정이 아직 없는 상태(신규 배포,
# 운영자 탈퇴 직후)에서는 누구든 그 주소로 가입해 다음 기동에 관리자 권한을 받아갈 수 있다.
# 값이 없으면 관리자 관련 자동 정리를 아예 수행하지 않는다(main.py의 enforce_roles 참고).
OWNER_ADMIN_EMAIL = _get("OWNER_ADMIN_EMAIL")
if IS_PRODUCTION and not OWNER_ADMIN_EMAIL:
    raise ConfigError(
        "[치명] OWNER_ADMIN_EMAIL이 설정되지 않았습니다. "
        "운영 환경에서는 관리자 계정을 명시해야 합니다."
    )
if not OWNER_ADMIN_EMAIL:
    print("[config] OWNER_ADMIN_EMAIL 미설정 → 관리자 권한 자동 부여/회수를 건너뜁니다.")

# ── AI 사회자(봇) 계정 ──
ADMIN_SEED_EMAIL = _get("ADMIN_SEED_EMAIL", "admin@admin.com")
# 참고: AI 사회자 봇 계정은 로그인이 차단되어 있어 비밀번호를 쓰지 않는다.
# (봇 생성 시 main.py가 임의 난수를 넣는다) 이 설정은 더 이상 필요하지 않아 제거했다.

# ── CORS ──
# 프론트엔드를 이 서버가 직접 서빙하므로(동일 출처) 평소에는 CORS 허용 목록이 필요 없다.
# 별도 도메인에서 API를 호출해야 하면 .env의 ALLOW_ORIGINS에 쉼표로 나열한다.
ALLOW_ORIGINS = [o.strip() for o in _get("ALLOW_ORIGINS").split(",") if o.strip()]

# 개발 환경에서는 포트를 자유롭게 바꿔 띄울 수 있도록 localhost의 모든 포트를 허용한다.
# (운영에서는 None이므로 ALLOW_ORIGINS에 적힌 출처만 허용된다.)
ALLOW_ORIGIN_REGEX = None if IS_PRODUCTION else r"http://(localhost|127\.0\.0\.1)(:[0-9]+)?"

if "*" in ALLOW_ORIGINS:
    raise ConfigError(
        "[치명] ALLOW_ORIGINS에 와일드카드(*)는 허용하지 않습니다. 허용할 출처를 명시적으로 나열하세요."
    )

# ── SMTP (비밀번호 재설정 메일) ──
SMTP_SERVER = _get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = _get_int("SMTP_PORT", 587)
SMTP_USERNAME = _get("SMTP_USERNAME")
SMTP_PASSWORD = _get("SMTP_PASSWORD")
SMTP_FROM_EMAIL = _get("SMTP_FROM_EMAIL", SMTP_USERNAME)

_SMTP_PLACEHOLDERS = {"your_gmail_username@gmail.com", "your_gmail_app_password"}
SMTP_CONFIGURED = bool(
    SMTP_USERNAME
    and SMTP_PASSWORD
    and SMTP_USERNAME not in _SMTP_PLACEHOLDERS
    and SMTP_PASSWORD not in _SMTP_PLACEHOLDERS
)

# ── 비밀번호 재설정 링크 ──
# 메일에 담을 링크의 기준 주소. 운영 도메인으로 반드시 교체해야 링크가 동작한다.
APP_BASE_URL = _get("APP_BASE_URL", "http://127.0.0.1:8001").rstrip("/")
PASSWORD_RESET_TTL_MINUTES = _get_int("PASSWORD_RESET_TTL_MINUTES", 30)

# ── 기타 외부 서비스 ──
GEMINI_API_KEY = _get("GEMINI_API_KEY")
