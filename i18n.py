"""응답 문구의 언어를 요청 단위로 들고 다니는 아주 작은 계층.

화면에서 고른 언어가 X-App-Lang 헤더로 들어온다. 그 값을 요청마다 여기에
담아 두고, 문구를 만들 때 m(한국어, 일본어)로 고른다.

main.py에 두었더니 auth.py에서 쓸 수 없었다. auth.py는 main.py가 불러오는
쪽이라 거꾸로 부르면 순환 참조가 된다. 그래서 두 모듈이 함께 기댈 수 있는
자리로 옮겼다.

기본값을 일본어로 둔 이유: 화면의 기본 언어가 일본어이고, 헤더가 없는
요청(직접 호출·크롤러)도 일본어를 받는 편이 서비스와 어긋나지 않는다.
"""

from contextvars import ContextVar

_REQ_LANG: ContextVar = ContextVar("req_lang", default="ja")

SUPPORTED = ("ko", "ja")


def set_request_lang(raw: str):
    """요청의 언어를 정하고, 되돌릴 토큰을 돌려준다.

    ContextVar라 요청끼리 값이 섞이지 않는다. 호출한 쪽이 끝나면
    reset_request_lang으로 반드시 되돌린다.
    """
    lang = (raw or "").strip().lower()
    return _REQ_LANG.set(lang if lang in SUPPORTED else "ja")


def reset_request_lang(token):
    _REQ_LANG.reset(token)


def current_lang() -> str:
    return _REQ_LANG.get()


def m(ko: str, ja: str) -> str:
    """사용자에게 보일 문구를 요청 언어에 맞춰 고른다."""
    return ko if _REQ_LANG.get() == "ko" else ja
