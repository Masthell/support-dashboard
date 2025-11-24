from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Схема для создания пользователя
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = "user"

# Схема для обновления пользователя
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None

# Схема для ответа (без пароля!)
class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    role: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # Работа с ORM объектами

# Схема для аутентификации
class UserLogin(BaseModel):
    email: EmailStr
    password: str