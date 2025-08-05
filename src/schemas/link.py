from sqlmodel import SQLModel, Field


class BookAuthorLink(SQLModel, table=True):
    book_id: int = Field(foreign_key="book.id", primary_key=True)
    author_id: int = Field(foreign_key="author.id", primary_key=True)