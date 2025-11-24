from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db, engine

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Support Dashboard API",
    description="API для системы поддержки пользователей",
    version="1.0.0"
)

# Простой эндпоинт для проверки
@app.get("/")
def read_root():
    return {"message": "Welcome to Support Dashboard API"}

# Эндпоинт для получения всех пользователей
@app.get("/users/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# Эндпоинт для создания пользователя
@app.post("/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь с таким email
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Создаем нового пользователя (пока без хэширования пароля)
    db_user = models.User(
        email=user.email,
        password=user.password,  # В будущем нужно хэшировать!
        full_name=user.full_name,
        role=user.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Эндпоинт для получения пользователя по ID
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
