import datetime
from datetime import timezone, timedelta
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from database import Base

def get_kst_now():
    return datetime.datetime.now(timezone(timedelta(hours=9))).replace(tzinfo=None)

# 1. USERS 테이블 (회원 계정)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    # 운영 권한(도서 삭제 등). 실제 사람 운영자에게만 부여한다.
    is_admin = Column(Boolean, default=False, nullable=False)
    # AI 사회자 같은 봇 페르소나 여부. 봇은 로그인할 수 없고 운영 권한도 갖지 않는다.
    is_bot = Column(Boolean, default=False, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nickname = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=get_kst_now)
    last_generation_at = Column(DateTime, nullable=True)  # "새 책 생성" 마지막 호출 시각 (1일 1회 제한용)
    # 비밀번호 최종 변경 시각. 이 시각보다 먼저 발급된 JWT는 무효로 처리한다(토큰 탈취 대응).
    password_changed_at = Column(DateTime, nullable=True)
    # 비밀번호 재설정 링크 토큰. 원문이 아닌 SHA-256 해시만 저장한다(DB 유출 시 재사용 방지).
    reset_token_hash = Column(String(64), nullable=True)
    reset_token_expires_at = Column(DateTime, nullable=True)

    # ORM Relationships
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")
    library_entries = relationship("Library", back_populates="user", cascade="all, delete-orphan")


# 2. BOOKS 테이블 (가상 도서 및 독서방)
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), index=True, nullable=False)
    author = Column(String(100), nullable=False)
    genre = Column(String(50), nullable=False)
    synopsis = Column(Text, nullable=False)
    tags = Column(String(255), nullable=False)  # 쉼표(,)로 구분되는 태그 문자열
    price = Column(String(50), default="₩14,000")
    color = Column(String(150), default="#7b5fb8")  # 책등 표지 색상 코드
    cover_image_url = Column(String(500), nullable=True) # AI 생성 표지 이미지 경로/URL
    endorsement_quote = Column(String(500), nullable=True)
    endorsement_attr = Column(String(100), nullable=True)
    publisher_review = Column(Text, nullable=True)

    opening_line = Column(Text, nullable=True)        # 소설의 첫 문장
    memorable_quote = Column(String(500), nullable=True) # 결정적 대사
    core_dilemma = Column(String(500), nullable=True)    # 핵심 토론 딜레마
    additional_questions = Column(Text, nullable=True)  # 추가 토론 질문 (파이프 '|' 구분)
    characters = Column(Text, nullable=True)             # 등장인물 (파이프 '|' 구분, "이름::한줄인상" 형식)
    page_count = Column(Integer, nullable=True)          # 책 페이지 수
    immersion_data = Column(Text, nullable=True)         # 가상 상세 도서 정보 (챕터, 리뷰, 트리비아 등 JSON)

    # 독서방 종료 시 AI 사회자가 남기는 총평. 아카이브 하단 「기록의 보관을 마치며」에 쓰인다.
    # 비어 있으면 프론트가 기존 고정 문구로 대체하므로 생성 실패가 화면을 깨지 않는다.
    closing_remark = Column(Text, nullable=True)
    # 일본어 번역본(JSON). 필드마다 컬럼을 두지 않고 한 덩어리로 보관한다.
    # 예: {"title": "...", "synopsis": "...", "closing_remark": "..."}
    i18n_ja = Column(Text, nullable=True)
    deadline_days = Column(Integer, default=10)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=get_kst_now)

    # ORM Relationships
    chat_messages = relationship("ChatMessage", back_populates="book", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="book", cascade="all, delete-orphan")
    library_entries = relationship("Library", back_populates="book", cascade="all, delete-orphan")


# 2-1. CANDIDATE_BOOKS 테이블 (책 생성 전 3가지 후보)
class CandidateBook(Base):
    __tablename__ = "candidate_books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    genre = Column(String(50), nullable=False)
    synopsis = Column(Text, nullable=False)
    tags = Column(String(255), nullable=False)
    price = Column(String(50), default="₩14,000")
    color = Column(String(150), default="#7b5fb8")
    cover_image_url = Column(String(500), nullable=True) # AI 생성 표지 이미지 경로/URL
    endorsement_quote = Column(String(500), nullable=True)
    endorsement_attr = Column(String(100), nullable=True)
    publisher_review = Column(Text, nullable=True)
    
    opening_line = Column(Text, nullable=True)
    memorable_quote = Column(String(500), nullable=True)
    core_dilemma = Column(String(500), nullable=True)
    additional_questions = Column(Text, nullable=True)
    characters = Column(Text, nullable=True)
    page_count = Column(Integer, nullable=True)
    immersion_data = Column(Text, nullable=True)
    
    status = Column(String(20), default="pending", nullable=False) # 'pending' (선택 대기), 'pool' (미선택 재사용 풀), 'adopted' (채택됨)
    # 이 후보를 만든 사용자. 아직 고르지 않은(pending) 후보를 그 사람에게만 다시 보여주는 데 쓴다.
    # 백그라운드 자동 보충으로 만들어진 후보는 주인이 없으므로 NULL이다.
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=get_kst_now)


# 3. CHAT_MESSAGES 테이블 (독서방 비동기 대화형 댓글)
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)  # 대화 본문 (Text 타입으로 문장 잘림 방지)
    reply_to_id = Column(Integer, ForeignKey("chat_messages.id", ondelete="SET NULL"), nullable=True)
    # 반응 카운트를 JSON 문자열로 저장
    # 사회자 시스템 메시지(첫 인사·폐회 인사)의 일본어 본문. 독자 감상은 비워 둔다.
    content_ja = Column(Text, nullable=True)
    reactions = Column(String(500), nullable=True, default=None)
    created_at = Column(DateTime, default=get_kst_now)

    # ORM Relationships
    book = relationship("Book", back_populates="chat_messages")
    user = relationship("User", back_populates="chat_messages")
    
    # Self-referencing relationship for reply quote feature
    replies = relationship("ChatMessage", cascade="all")
    parent_reply = relationship("ChatMessage", remote_side=[id], backref=backref("child_replies", overlaps="replies"), overlaps="replies")


# 6. RATINGS 테이블 (도서 별점 정보)
class Rating(Base):
    __tablename__ = "ratings"
    # 한 사람은 한 책에 평점을 한 번만 남긴다 (DB 차원에서 강제)
    __table_args__ = (UniqueConstraint("book_id", "user_id", name="uq_ratings_book_user"),)

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)  # 1 ~ 5 점

    # ORM Relationships
    book = relationship("Book", back_populates="ratings")
    user = relationship("User", back_populates="ratings")


# 7. LIBRARY 테이블 (내 서재 보관함)
class Library(Base):
    __tablename__ = "library"
    # 같은 책을 서재에 두 번 담지 않는다
    __table_args__ = (UniqueConstraint("user_id", "book_id", name="uq_library_user_book"),)

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    saved_at = Column(DateTime, default=get_kst_now)

    # ORM Relationships
    user = relationship("User", back_populates="library_entries")
    book = relationship("Book", back_populates="library_entries")


# 8. PAST_CHAT_MESSAGES 테이블 (독서방 종료 후 채팅 기록 보관 전용 창고)
# 메인 chat_messages 테이블의 데이터가 많아질 때 이곳으로 이전하여 메인 DB를 경량화합니다.
class PastChatMessage(Base):
    __tablename__ = "past_chat_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)

    # 탈퇴 회원의 기록도 보존되도록 user_id는 FK 없이 순수 정수로 저장
    user_id = Column(Integer, nullable=False)
    # 닉네임을 직접 저장 (탈퇴 후에도 닉네임이 기록에 영구 보존됨)
    user_nickname = Column(String(50), nullable=False)

    content = Column(Text, nullable=False)

    # 답장 원본 정보: 원본 메시지가 삭제되어도 인용이 보존되도록 비정규화하여 저장
    reply_to_id = Column(Integer, nullable=True)
    reply_to_user = Column(String(50), nullable=True)
    reply_to_content = Column(Text, nullable=True)

    # 사회자 시스템 메시지의 일본어 본문 (보관본에도 함께 옮긴다)
    content_ja = Column(Text, nullable=True)
    reactions = Column(String(500), nullable=True, default=None)

    original_created_at = Column(DateTime, nullable=False)  # 원본 채팅 작성 시각
    archived_at = Column(DateTime, default=get_kst_now)     # 아카이브 이전(Migration) 시각

    # 책 정보 참조 (책이 삭제되면 CASCADE로 함께 삭제)
    book = relationship("Book", backref="past_chat_messages")
