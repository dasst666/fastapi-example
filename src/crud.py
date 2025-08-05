from src.database import SessionDep
from src.schemas.book import Book, BookBase


def create_book(book: BookBase, session: SessionDep):
    db_book = Book(**book.dict())
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book
