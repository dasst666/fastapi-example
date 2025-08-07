from typing import List
from sqlmodel import Relationship, SQLModel, Field

from src.schemas.link import BookAuthorLink

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .book import Book

class AuthorBase(SQLModel):
    first_name: str
    last_name: str
    age: int

class Author(AuthorBase, table=True):
    id: int | None = Field(default = None, primary_key = True)

    books: List["Book"] = Relationship(
        back_populates="authors",
        link_model=BookAuthorLink
    )

class AuthorPublic(AuthorBase):
    id: int