import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.books.crud import (
    get_book,
    get_book_by_id,
    create_book,
    delete_book,
    update_book,
    count_books,
)
from app.api.schemas import Response, BookSchema
from app.db import get_db
from app.utils.auth_middleware import get_current_user

router = APIRouter()


@router.get("/{book_id}")
async def get_book_by_id_route(
    book_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _book = get_book_by_id(db, book_id)
    return Response(code=200, status="ok", message="success", result=_book).model_dump()


@router.get("/")
async def get_books_route(
    req: Request,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    _books = get_book(
        db,
        limit=limit,
        skip=skip,
        order_by=req.query_params.get("order"),
        search=req.query_params.get("search"),
    )
    _count_of_books = count_books(db)

    return Response(
        code=200,
        status="ok",
        message="success",
        result=[
            {
                "id": book.id,
                "name": book.name,
                "book_url": book.book_url,
                "created_at": book.created_at,
                "updated_at": book.updated_at,
            }
            for book in _books
        ],
        total=_count_of_books,
        info={"result": limit, "page": skip},
    ).dict()


@router.post("/")
async def create_book_route(
    book: BookSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    create_book(db, book)
    return Response(code=201, status="ok", message="created").dict()


@router.delete("/{book_id}")
async def delete_book_route(
    book_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    delete_book(db, book_id)
    return Response(
        code=200,
        status="ok",
        message="deleted",
    ).model_dump()


@router.put("/{book_id}")
async def update_book_route(
    book_id: uuid.UUID,
    book: BookSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _book = update_book(db, book, book_id)
    return Response(code=200, status="ok", message="updated", result=_book).model_dump()
