from enum import Enum
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional


class UserRole(str, Enum):
    """Допустимые роли пользователей в системе"""
    USER = "user"
    OPERATOR = "operator" 
    MANAGER = "manager"
    ADMIN = "admin"


class UserCreate(BaseModel):
    """Схема регистрации пользователя"""
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    full_name: Optional[str] = Field(None, max_length=100)
    role: UserRole = Field(default=UserRole.USER, description="Default role is 'user'")

    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Убедитесь, что пароль соответствует минимальным требованиям безопасности"""
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if v.lower() == 'password':
            raise ValueError('Пароль слишком прост')
        return v


class UserUpdate(BaseModel):
    """Схема обновления профиля пользователя"""
    
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    role: Optional[UserRole] = None


class UserResponse(BaseModel):
    """Схема для пользовательских данных в ответах API (исключает конфиденциальные поля)"""
    id: int
    email: str
    full_name: Optional[str]
    role: UserRole
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # Совместимость с объектами ORM SQLAlchemy


class UserLogin(BaseModel):
    """Схема для аутентификации пользователя."""
    email: EmailStr
    password: str = Field(..., min_length=1, description="Password cannot be empty")
