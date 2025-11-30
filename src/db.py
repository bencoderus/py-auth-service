from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DATABASE_URL = getenv("DB_CONNECTION_STRING")

if not DATABASE_URL:
    raise ValueError("DB_CONNECTION_STRING is not set")

DB_CONNECTION_STRING = DATABASE_URL.replace("postgresql", "postgresql+asyncpg")

engine = create_async_engine(
    DB_CONNECTION_STRING,
    echo=False,
    future=True
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
