from fastapi import APIRouter, HTTPException
from sqlmodel import select

from src.crud.author import create_author, delete_author
from src.database import SessionDep
from src.schemas.author import Author, AuthorBase

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)

@router.post("/")
def create_author_route(author: AuthorBase, session: SessionDep):
    return create_author(author, session)

@router.delete("/{author_id}")
def delete_author_route(author_id: int, session: SessionDep):
    success = delete_author(author_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"success": True}

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
