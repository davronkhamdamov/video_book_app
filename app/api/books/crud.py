import datetime
import uuid
from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.api.models import Books
from app.api.schemas import BookSchema


def get_book(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    order_by: Optional[str] = None,
    search: Optional[str] = None,
):
    if skip < 0:
        skip = 0

    query = db.query(Books)
    if search:
        search = f"%{search}%"
        query = query.filter(or_(Books.name.ilike(search)))

    if order_by == "descend":
        query = query.order_by(Books.name.desc())
    elif order_by == "ascend":
        query = query.order_by(Books.name.asc())
    else:
        query = query.order_by(Books.created_at.desc())

    return query.offset(skip * limit).limit(limit).all()


def count_books(db: Session):
    return db.query(func.count(Books.id)).scalar()


def get_book_by_id(db: Session, book_id: uuid.UUID):
    return db.query(Books).filter(Books.id == book_id).first()


def create_book(db: Session, book: BookSchema):
    _book = Books(
        name=book.name,
        book_url=book.book_url,
        created_at=datetime.datetime.now(),
    )
    db.add(_book)
    db.commit()
    db.refresh(_book)
    return _book


def delete_book(db: Session, book_id: uuid.UUID):
    db.query(Books).filter(Books.id == book_id).delete()
    db.commit()


def update_book(db: Session, book: BookSchema, book_id: uuid.UUID):
    _book = get_book_by_id(db=db, book_id=book_id)
    _book.name = book.name
    _book.book_url = book.book_url
    _book.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(_book)
    return _book
