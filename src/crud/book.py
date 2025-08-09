from sqlmodel import select
from src.database import SessionDep
from src.schemas.author import Author
from src.schemas.book import Book, BookCreate


def create_book(book: BookCreate, session: SessionDep):
    db_book = Book(title=book.title)

    if book.author_ids:
        authors = session.exec(select(Author).where(Author.id.in_(book.author_ids))).all()
        db_book.authors = authors

    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

def delete_book(book_id: int, session: SessionDep):
    db_book = session.get(Book, book_id)
    if not db_book:
        return False
    session.delete(db_book)
    session.commit()
    return True