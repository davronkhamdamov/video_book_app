import uuid
from datetime import datetime
from typing import Generic, TypeVar, Optional

from pydantic import BaseModel

T = TypeVar("T")


class UserSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str = None
    surname: str = None
    login: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class VideoSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str = None
    video_url: str = None
    description: str = None
    duration: str = None
    capacity: str = None
    type: Optional[str] = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class BookSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str = None
    book_url: str = None
    description: str = None
    book_author: str = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class BookReadingSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    user_id: uuid.UUID = None
    book_id: uuid.UUID = None
    is_read: bool = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class VideoViewSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    user_id: uuid.UUID = None
    video_id: uuid.UUID = None
    latest_time: str = None
    is_viewed: bool = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class Response(BaseModel, Generic[T]):
    code: int
    status: str
    message: str
    total: Optional[int] = None
    result: Optional[T] = None
    info: Optional[dict] = None
    role: Optional[str] = None


class LoginSchema(BaseModel):
    login: str
    password: str
