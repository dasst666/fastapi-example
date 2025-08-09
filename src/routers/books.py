from fastapi import APIRouter, HTTPException
from sqlmodel import select

from src.crud.book import create_book, delete_book
from src.database import SessionDep
from src.schemas.book import Book, BookBase, BookCreate, BookPublic

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}}
)

@router.post("/")
def create_book_route(book: BookCreate, session: SessionDep):
    return create_book(book, session)

@router.delete("/{book_id}")
def delete_book_route(book_id: int, session: SessionDep):
    success = delete_book(book_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"success": True}

@router.get("/{book_id}", response_model=BookPublic)
def read_book(session: SessionDep, book_id: int):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    return book

@router.get("/")
def read_books(session: SessionDep):
    books = session.exec(select(Book)).all()
    return books