from fastapi import APIRouter, Depends, HTTPException  
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select  
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db
from app.models.user import User  
from app.schemas.user import UserLogin, UserCreate, UserResponse
from app.core.security import verify_password, create_access_token, hash_password
from app.core.dependencies import get_current_user
from app.core.exceptions import (
    InvalidCredentialsException, 
    EmailAlreadyExistsException,
    UserNotFoundException
)


router = APIRouter()

# Допустимые роли пользователей для регистрации
VALID_ROLES = ["user", "operator", "manager", "admin"]


@router.post("/login")
async def login(  
    user_data: UserLogin, 
    db: AsyncSession = Depends(get_db)  
):
    """Аутентифицировать пользователя и вернуть токен доступа JWT."""
    # Find user by email
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()
    
    # Verify credentials
    if not user or not verify_password(user_data.password, user.password):
        raise InvalidCredentialsException()
    
    # Генерация токена JWT с данными пользователя
    access_token = create_access_token(
        data={
            "sub": str(user.id), 
            "email": user.email,
            "role": user.role  # Include role for authorization
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "role": user.role 
    }


@router.post("/register", response_model=UserResponse)
async def register(  
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_db)  
):
    """регистрация нового юзера"""
    # Проверить наличие существующего пользователя
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise EmailAlreadyExistsException()
    
    # проверка роли
    role = user_data.role or "user"
    if role not in VALID_ROLES:
        raise HTTPException(400, f"Invalid role. Must be one of: {VALID_ROLES}")
    
    hashed_password = hash_password(user_data.password)

    db_user = User(
        email=user_data.email,
        password=hashed_password,
        full_name=user_data.full_name,
        role=role
    )

    try:
        db.add(db_user)
        await db.commit()  
        await db.refresh(db_user) 
        return db_user
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "Database error during registration")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(  
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)  
):
    """Получить информацию о текущем авторизованном пользователе."""
    try:
        user_id = int(current_user["sub"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(401, "Invalid token payload")
    
    # Получить свежие данные пользователя из базы данных
    result = await db.execute(select(User).where(User.id == user_id))  
    user = result.scalar_one_or_none()

    if not user:
        raise UserNotFoundException()
    
    return user