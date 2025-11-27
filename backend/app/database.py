from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

Base = declarative_base()

# Используем DATABASE_URL из переменных окружения
engine = create_engine(
    settings.DATABASE_URL,  
    echo=True,  
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_recycle=3600    # Переподключение каждый час
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

def create_tables():
    Base.metadata.create_all(bind=engine)