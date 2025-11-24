from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import Base  # Импортируем Base из моделей


# URL базы данных из переменных окружения
DATABASE_URL = "sqlite:///./support.db"

# Движок БД
engine = create_engine(DATABASE_URL)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создание таблиц (для начальной настройки)
def create_tables():
    Base.metadata.create_all(bind=engine)