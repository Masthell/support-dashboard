from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  
from sqlalchemy import select  
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.security import hash_password 
from app.core.dependencies import get_current_user
from app.core.exceptions import ( 
    EmailAlreadyExistsException,
    UserNotFoundException
)


router = APIRouter()


@router.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_db)
): 
    """создать нового юзера"""
    # Проверить, существует ли пользователь
    result = await db.execute(select(User).where(User.email == user_data.email)) 
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise EmailAlreadyExistsException()  
    
    # Создать нового пользователя с хэшированным паролем
    hashed_password = hash_password(user_data.password)  
    
    db_user = User(
        email=user_data.email,
        password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role or "user"
    )
    
    try:
        db.add(db_user)
        await db.commit()  
        await db.refresh(db_user)  
        return db_user
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "Database error during user creation")


@router.get("/users/me", response_model=UserResponse)  
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)  
):  
    """Получить информацию о текущем авторизованном пользователе."""
    user_id = int(current_user["sub"]) # Текущие данные пользователя
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise UserNotFoundException()   #  если пользователь больше не существует в базе данных
    
    return user  


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Получить пользователя по ID (требуется аутентификация)."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise UserNotFoundException()
    
    return user


# АДМИН ЭНДПОИНТЫ
@router.get("/admin/users")
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user) 
):
    """Получить всех пользователей (только для администратора)"""
    # Проверить, является ли текущий пользователь администратором
    if current_user.get("role") != "admin":
        raise HTTPException(403, "Admin access required")
    
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.patch("/admin/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    role_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user) 
):
    """повышение пользователя только для админа"""
    # Проверить права администратора
    if current_user.get("role") != "admin":
        raise HTTPException(403, "Admin access required")
    
    # Подтвердить роль
    valid_roles = ["user", "operator", "manager", "admin"]
    new_role = role_data.get("role")
    if new_role not in valid_roles:
        raise HTTPException(400, f"Invalid role. Must be one of: {valid_roles}")
    
    # Найти и обновить пользователя
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise UserNotFoundException()
    
    try:
        user.role = new_role
        await db.commit()
        await db.refresh(user)
        
        return {"message": f"Role updated to {user.role}", "user": user}
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "Database error during role update")