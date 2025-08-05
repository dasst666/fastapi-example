from fastapi import APIRouter, HTTPException
from sqlmodel import select

from src.crud import create_book
from src.database import SessionDep
from src.schemas.book import Book, BookBase, BookPublic

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}}
)

@router.post("/")
def create_book_route(book: BookBase, session: SessionDep):
    return create_book(book, session)

@router.delete("/{book_id}")
def delete_book(book_id: int, session: SessionDep):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"sucess": True}

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