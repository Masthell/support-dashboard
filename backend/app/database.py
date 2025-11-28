from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import make_url
from urllib.parse import quote
from app.core.config import settings

Base = declarative_base()

def create_async_database_url(database_url: str) -> str:
    """Создает асинхронный URL правильным экранированием"""
    original_url = make_url(database_url)
    
    escaped_password = quote(original_url.password, safe='')
    
    async_url = (
        f"mysql+aiomysql://{original_url.username}:{escaped_password}"
        f"@{original_url.host}:{original_url.port}/{original_url.database}"
    )
    
    return async_url

# Создать асинхронный движок базы данных с объединением подключений
async_database_url = create_async_database_url(settings.DATABASE_URL)

engine = create_async_engine(
    async_database_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={"connect_timeout": 10}
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
