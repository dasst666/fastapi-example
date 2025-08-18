from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from src.security import create_access_token
from src.database import SessionDep
from src.schemas.token import Token
from src.schemas.user import User
from src.security import verify_password


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login", response_model=Token)
def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Неверный Email или Пароль", 
            headers={"WWW-Authenticate": "Bearer"}
            )
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}