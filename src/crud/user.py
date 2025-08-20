from sqlmodel import select

from src.database import SessionDep
from src.schemas.user import User, UserCreate
from src.security import hash_password


def create_user(session: SessionDep, user_data: UserCreate):
    hashed_pwd = hash_password(user_data.password)
    user = User(email=user_data.email, hashed_password=hashed_pwd)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_email(session: SessionDep, email: str):
    return session.exec(select(User).where(User.email == email)).first()
