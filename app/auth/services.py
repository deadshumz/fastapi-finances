from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions import UserAlreadyExistsException
from app.auth.models import User
from app.auth.schemas import UserCreate, UserRead
from app.auth.utils import hash_password


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[UserRead]:
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    db_users = result.scalars().all()

    users = []
    for user in db_users:
        users.append(UserRead.model_validate(user))

    return users


async def get_user_by_username(db: AsyncSession, username: str) -> UserRead | None:
    query = select(User).filter_by(username=username)
    result = await db.execute(query)
    db_user = result.scalars().first()
    user = UserRead.model_validate(db_user)
    return user


async def get_user_by_email(db: AsyncSession, email: EmailStr) -> UserRead | None:
    query = select(User).filter_by(email=email)
    result = await db.execute(query)
    db_user = result.scalars().first()
    user = UserRead.model_validate(db_user)
    return user


async def add_user(db: AsyncSession, user: UserCreate) -> User:
    existing_user_by_username = await get_user_by_username(db, user.username)
    if existing_user_by_username:
        raise UserAlreadyExistsException("User with this username already exists")

    existing_user_by_email = await get_user_by_email(db, user.email)
    if existing_user_by_email:
        raise UserAlreadyExistsException("User with this email already exists")

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
