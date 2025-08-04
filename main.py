from typing import Annotated
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import select

from database import SessionDep, create_db_and_tables
from models import Book

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/books/")
def create_book(book: Book, session: SessionDep) -> Book:
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, session: SessionDep):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"sucess": True}

@app.get("/books/{book_id}")
def read_book(session: SessionDep, book_id: int):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    return book

@app.get("/books/")
def read_books(session: SessionDep):
    books = session.exec(select(Book)).all()
    return books

#------------------------------------------------------- 

@app.get("/hello/{name}")
def hello_world(name, skip = 0):
    return {"message": name, "skip": skip}

class User(BaseModel):
    name: str
    number: int

@app.post("/user")
def create_user(user: User):
    return user

@app.get("/multiply/{a}/{b}")
def multiply(a: int, b: int):
    if a > 0 and b > 0:
        return {"result": a * b}
    else:
        raise HTTPException(status_code=400, detail="a and b must be greater than 0")
    
@app.get("/users/filter")
def filter_users(
    min_age: Annotated[int, Query(gt=0)], 
    max_age: Annotated [int | None, Query(gt=0, le=150)]):
    if max_age is not None and max_age < min_age:
        raise HTTPException(status_code=400, detail="max age is not lower than min age")
    return {"filtered": True, "min_age": min_age, "max_age": max_age}

    