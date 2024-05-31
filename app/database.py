from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import settings

engine = create_async_engine(str(settings.pg_dsn))
AsyncSessionLocal = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
