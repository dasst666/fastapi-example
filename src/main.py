from fastapi import FastAPI


from src.database import create_db_and_tables
from src.routers import auth, authors, books, users


app = FastAPI()

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


    