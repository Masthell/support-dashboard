from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.core.exceptions import InvalidTokenException
from app.core.exceptions import ForbiddenException

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise NotAuthenticatedException()  
    
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise InvalidTokenException()
    return payload

def require_role(required_role: str):
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") != required_role and current_user.get("role") != "admin":
            from app.core.exceptions import ForbiddenException
            raise ForbiddenException(detail=f"Requires {required_role} role")
        return current_user
    return role_checker