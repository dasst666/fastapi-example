from typing import Annotated, List
from sqlmodel import Relationship, SQLModel, Field

from src.schemas.link import BookAuthorLink

class BookBase(SQLModel):
    title: str = Field(index=True)
    author: str 

class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    authors: List["Author"] = Relationship(
        back_populates="books",
        link_model=BookAuthorLink
    )

class BookPublic(BookBase):
    id: int