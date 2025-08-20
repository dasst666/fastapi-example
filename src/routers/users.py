from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from src.crud.user import create_user, get_user_by_email
from src.database import SessionDep
from src.schemas.user import User, UserCreate, UserPublic

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, session: SessionDep):
    existing_user = get_user_by_email(session, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    return create_user(session, user_data)


@router.get("/")
def get_user_list(session: SessionDep):
    return session.exec(select(User)).all()
