import datetime
import uuid

from sqlalchemy import Column, UUID, String, DateTime, Boolean, ForeignKey

from app.db import Base, engine


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    surname = Column(String, index=True, nullable=False)
    login = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


class Books(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    book_url = Column(String, nullable=False)
    description = Column(String, nullable=True)
    book_author = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


class Video(Base):
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    video_url = Column(String, nullable=False)
    description = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    capacity = Column(String, nullable=True)
    type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


class VideoView(Base):
    __tablename__ = "video_watch"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    video_id = Column(UUID(as_uuid=True), ForeignKey("videos.id"), nullable=False)
    latest_time = Column(String, nullable=True)
    is_viewed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


class BookReading(Base):
    __tablename__ = "book_reading"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_viewed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


Base.metadata.create_all(bind=engine)
