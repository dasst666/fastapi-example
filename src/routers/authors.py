from fastapi import APIRouter, HTTPException
from sqlmodel import select

from src.database import SessionDep
from src.schemas.author import Author, AuthorBase

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)

@router.post("/")
def create_author(author: AuthorBase, session: SessionDep):
    db_author = Author(**author.dict())
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author

@router.get("/{author_id}")
def get_author(author_id: int, session: SessionDep):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.get("/")
def get_authors(session: SessionDep):
    authors = session.exec(select(Author)).all()
    return authors

@router.delete("/{author_id}")
def delete_author(author_id: int, session: SessionDep):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()