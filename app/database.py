from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Database configuration
# Use /data directory if it exists (Fly.io volume), otherwise use local directory
db_path = os.getenv("DATABASE_PATH", "/data/charity_data.db" if os.path.exists("/data") else "./charity_data.db")
# Ensure parent directory exists
Path(db_path).parent.mkdir(parents=True, exist_ok=True)
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_path}")

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session maker
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """Get database session."""
    async with async_session() as session:
        yield session


async def init_db() -> None:
    """Initialize database and create tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()
