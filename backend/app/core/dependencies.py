from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import verify_token
from app.core.exceptions import (
    ForbiddenException,
    NotAuthenticatedException
)

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Зависимость для получения текущего пользователя из токена JWT."""
    if not credentials:
        raise NotAuthenticatedException()
    
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        # Заменили на существующий Exception
        raise NotAuthenticatedException(detail="Invalid token")
        
    return payload


def require_role(required_role: str):
    """Фабрика зависимостей для контроля доступа на основе ролей."""
    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        user_role = current_user.get("role")
        
        # Администратор имеет доступ ко всему
        if user_role == "admin":
            return current_user
            
        # Проверить, имеет ли пользователь необходимую роль
        if user_role != required_role:
            raise ForbiddenException(detail=f"Requires {required_role} role")
            
        return current_user
        
    return role_checker


async def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """Зависимость, требующая роли администратора."""
    if current_user.get("role") != "admin":
        raise ForbiddenException(detail="Admin access required")
    return current_user


async def require_operator_or_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """Зависимость, требующая роли оператора или администратора.
    Для твоего проекта можно удалить или адаптировать, если нет роли 'operator'."""
    user_role = current_user.get("role")
    if user_role not in ["operator", "admin"]:
        raise ForbiddenException(detail="Operator or admin access required")
    return current_user
