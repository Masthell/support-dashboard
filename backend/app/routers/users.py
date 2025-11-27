from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  
from sqlalchemy import select  
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password 
from app.core.dependencies import get_current_user

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)): 
    # ПРОВЕРКА на существующего пользователя 
    result = await db.execute(select(User).where(User.email == user_data.email)) 
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    hashed_password = hash_password(user_data.password)  
    
    db_user = User(
        email=user_data.email,
        password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role or "user"
    )
    
    db.add(db_user)
    await db.commit()  
    await db.refresh(db_user)  
    return db_user

@router.get("/users/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):  
    return {
        "message": "Это защищенный эндпоинт!",
        "user_data": current_user
    }