from typing import Annotated
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from src.database import create_db_and_tables
from src.routers import authors, books


app = FastAPI()

app.include_router(books.router)
app.include_router(authors.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

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

    