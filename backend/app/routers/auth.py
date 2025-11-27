from fastapi import APIRouter, Depends, HTTPException  
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select  
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

@router.post("/login")
async def login(  
    user_data: UserLogin, 
    db: AsyncSession = Depends(get_db)  
):

    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(user_data.password, user.password):
        raise InvalidCredentialsException()
    
    access_token = create_access_token(
        data={
            "sub": str(user.id), 
            "email": user.email,
            "role": user.role 
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
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise EmailAlreadyExistsException()
    
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

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(  
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)  
):
    user_id = int(current_user["sub"])
    
    result = await db.execute(select(User).where(User.id == user_id))  
    user = result.scalar_one_or_none()

    if not user:
        raise UserNotFoundException()
    
    return user