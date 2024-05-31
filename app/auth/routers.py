from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import UserIn, UserOut
from app.database import get_db
from app.auth.services import add_user, get_user_by_username, get_users

router = APIRouter()


@router.get("/")
async def read_users(db: AsyncSession = Depends(get_db)) -> list[UserOut]:
    db_users = await get_users(db)
    return db_users

@router.post("/")
async def create_user(user: Annotated[UserIn, Depends()], db: AsyncSession = Depends(get_db)) -> UserOut:
    db_user_by_id = get_user_by_username(db, user.username)
    if db_user_by_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")

    db_user = await add_user(db, user)
    return db_user
