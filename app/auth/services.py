import re
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.schemas import UserIn
from app.auth.utils import hash_password


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    return users


async def add_user(db: AsyncSession, user: UserIn) -> User:
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    db_user = User(**user.model_dump())

    db.add(db_user)

    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e

    await db.refresh(db_user)
    return db_user

async def get_user_by_username(db: AsyncSession, username: str) -> User:
    query = select(User).filter_by(username=username)
    result = await db.execute(query)
    user = result.scalars().one()
    return user
