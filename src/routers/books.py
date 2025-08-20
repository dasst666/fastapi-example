from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from src.crud.book import create_book, delete_book
from src.database import SessionDep
from src.dependencies import get_current_user
from src.schemas.book import Book, BookCreate, BookPublic
from src.schemas.user import RoleEnum, User

router = APIRouter(
    prefix="/books", tags=["books"], responses={404: {"description": "Not found"}}
)


@router.post("/")
def create_book_route(
    book: BookCreate, session: SessionDep, user: User = Depends(get_current_user)
):
    return create_book(book, session)


@router.delete("/{book_id}")
def delete_book_route(
    book_id: int, session: SessionDep, user: User = Depends(get_current_user)
):
    if user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Недостаточно прав для удаления")
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
