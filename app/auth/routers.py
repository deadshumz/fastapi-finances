from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions import UserAlreadyExistsException
from app.auth.schemas import UserCreate, UserRead
from app.auth.services import add_user, get_users
from app.database import get_db

router = APIRouter()


@router.get("/")
async def read_users(db: AsyncSession = Depends(get_db)) -> list[UserRead]:
    db_users = await get_users(db)
    return db_users


@router.post("/")
async def create_user(
    user: Annotated[UserCreate, Depends()], db: AsyncSession = Depends(get_db)
) -> UserRead:
    try:
        db_user = await add_user(db, user)
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        ) from e

    return db_user
