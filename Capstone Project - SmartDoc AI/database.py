from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)


class Base(DeclarativeBase):
    pass
