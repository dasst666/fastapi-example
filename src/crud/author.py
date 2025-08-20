from src.database import SessionDep
from src.schemas.author import Author, AuthorBase


def create_author(author: AuthorBase, session: SessionDep):
    db_author = Author(**author.dict())
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


def delete_author(author_id: int, session: SessionDep):
    author = session.get(Author, author_id)
    if not author:
        return False
    session.delete(author)
    session.commit()
    return True
