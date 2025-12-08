from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.core.config import settings

# Create async engine
# Parse database URL
database_url = settings.DATABASE_URL
if "postgresql://" in database_url:
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

# Handle sslmode for asyncpg
connect_args = {}
if "?sslmode=" in database_url:
    database_url = database_url.split("?")[0]
    connect_args["ssl"] = "require"

engine = create_async_engine(
    database_url,
    echo=False,
    future=True,
    connect_args=connect_args,
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
