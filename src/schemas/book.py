from typing import Annotated, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.schemas.author import Author
from src.schemas.link import BookAuthorLink


class BookBase(SQLModel):
    title: str = Field(index=True)


class BookCreate(BookBase):
    author_ids: Optional[List[int]] = []


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    authors: List[Author] = Relationship(
        back_populates="books", link_model=BookAuthorLink
    )


class BookPublic(BookBase):
    id: int
    authors: List["Author"] = []
