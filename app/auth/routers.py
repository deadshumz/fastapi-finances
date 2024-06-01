from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions import UserAlreadyExistsException
from app.auth.schemas import Token, UserCreate, UserRead
from app.auth.services import add_user, authenticate_user, get_users
from app.auth.utils import create_access_token
from app.config import settings
from app.database import get_db

router = APIRouter()


@router.get("/")
async def read_users(db: AsyncSession = Depends(get_db)) -> list[UserRead]:
    db_users = await get_users(db)
    return db_users


@router.post("/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserRead:
    try:
        db_user = await add_user(db, user)
    except UserAlreadyExistsException as err:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        ) from err

    return db_user


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        form_data.username, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
